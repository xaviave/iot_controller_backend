import datetime
import random
import string

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC
from features.products_controller.grpc import (
    products_controller_pb2,
    products_controller_pb2_grpc,
)
from features.products_controller.views.category import CategoryService
from features.products_controller.views.products.coffee_machine import (
    CoffeeMachineService,
)
from features.products_controller.views.products.led.led_mode import LedModeService
from features.products_controller.views.products.led.led_panel import LedPanelService
from features.products_controller.views.project import ProjectService
from freezegun import freeze_time
from google.protobuf import json_format


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestProject(TransactionTestCase):
    """
    gRPC use proto3 that doesn't distinguish 0 and null
    so the return message will not be serialized with the null values.
    If one value is 0 or False, it will not be in the Response.
    """

    @property
    def _ignored_key(self) -> list:
        return ["polymorphicCtype"]

    @freeze_time("2024-02-02 03:21:34")
    def _clean_dict_response(self, d: dict) -> dict:
        clean_dict = {}
        for k, v in d.items():
            if k == "pubDate":
                clean_dict[k] = datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
            elif k not in self._ignored_key:
                clean_dict[k] = v
        return clean_dict

    def clean_response(self, res: dict) -> dict:
        if "results" in res.keys():
            return {"results": [self._clean_dict_response(d) for d in res["results"]]}
        return self._clean_dict_response(res)

    def setUp(self):
        self.category_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_CategoryControllerServicer_to_server,
            CategoryService.as_servicer(),
        )
        self.led_mode_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_LedModeControllerServicer_to_server,
            LedModeService.as_servicer(),
        )
        self.led_panel_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_LedPanelControllerServicer_to_server,
            LedPanelService.as_servicer(),
        )
        self.coffee_machine_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_CoffeeMachineControllerServicer_to_server,
            CoffeeMachineService.as_servicer(),
        )
        self.project_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_ProjectControllerServicer_to_server,
            ProjectService.as_servicer(),
        )

    def tearDown(self):
        self.category_fake_grpc.close()
        self.led_mode_fake_grpc.close()
        self.led_panel_fake_grpc.close()
        self.coffee_machine_fake_grpc.close()
        self.project_fake_grpc.close()

    async def create_product(self) -> list[str]:
        # Create Category Object
        category_grpc_stub = self.category_fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)
        request = products_controller_pb2.CategoryRequest(
            name="".join(random.choice(string.ascii_lowercase) for _ in range(20))
        )
        category = await category_grpc_stub.Create(request)

        # Create LedMode Object
        led_mode_grpc_stub = self.led_mode_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)
        request = products_controller_pb2.LedModeRequest(
            name="".join(random.choice(string.ascii_lowercase) for _ in range(20))
        )
        led_mode = await led_mode_grpc_stub.Create(request)

        # Create CoffeeMachine Object
        coffee_machine_grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )
        request = products_controller_pb2.CoffeeMachineRequest(
            name="".join(random.choice(string.ascii_lowercase) for _ in range(20)),
            status=1,
            heat=110.01,
            water_level=1,
            used_water_level=2,
            coffee_level=1,
            filter_position=True,
            mode_value=1,
            categories=[category.id],
        )
        coffee_machine = await coffee_machine_grpc_stub.Create(request)

        # Create LedPanel Object
        led_panel_grpc_stub = self.led_panel_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.LedPanelControllerStub
        )
        request = products_controller_pb2.LedPanelRequest(
            name="".join(random.choice(string.ascii_lowercase) for _ in range(20)),
            status=3,
            brightness=0.05,
            mode=led_mode.id,
            categories=[category.id],
        )
        led_panel = await led_panel_grpc_stub.Create(request)
        return [coffee_machine.uuid, led_panel.uuid]

    @freeze_time("2024-02-02 03:21:34")
    async def test_async_create_project(self):
        grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Project Object
        products = await self.create_product()
        project_date = datetime.datetime.now()
        project_owner = await sync_to_async(User.objects.create)(username="hannah montana", password="12345")
        request = products_controller_pb2.ProjectRequest(
            name="project smth",
            owner=project_owner.id,
            pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products,
        )
        create_res = await grpc_stub.Create(request)

        # Check one Project dataset
        res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "id": create_res.id,
                        "name": "project smth",
                        "pubDate": project_date,
                        "owner": project_owner.id,
                        "products": products,
                    }
                ]
            },
        )

    @freeze_time("2024-02-02 03:21:34")
    async def test_async_destroy_project(self):
        grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)

        # Create Project Object
        products = await self.create_product()
        project_date = datetime.datetime.now()
        project_owner = await sync_to_async(User.objects.create)(username="21 savage", password="21")
        request = products_controller_pb2.ProjectRequest(
            name="american dream",
            owner=project_owner.id,
            pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products,
        )
        create_res = await grpc_stub.Create(request)

        # Check one Project dataset
        res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "id": create_res.id,
                        "name": "american dream",
                        "pubDate": project_date,
                        "owner": project_owner.id,
                        "products": products,
                    }
                ]
            },
        )

        # Delete Project Object
        request = products_controller_pb2.ProjectDestroyRequest(id=create_res.id)
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
        self.assertListEqual(list(res.results), [])

    @freeze_time("2024-02-02 03:21:34")
    async def test_async_list_project(self):
        grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)

        # Create Project Object
        products_0 = await self.create_product()
        project_date_0 = datetime.datetime.now()
        project_owner_0 = await sync_to_async(User.objects.create)(username="wow", password="12345")
        request = products_controller_pb2.ProjectRequest(
            name="project 1",
            owner=project_owner_0.id,
            pub_date=project_date_0.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products_0,
        )
        create_res_0 = await grpc_stub.Create(request)

        products_1 = await self.create_product()
        project_date_1 = datetime.datetime.now()
        project_owner_1 = await sync_to_async(User.objects.create)(username="test test", password="12345")
        request = products_controller_pb2.ProjectRequest(
            name="project 2",
            owner=project_owner_1.id,
            pub_date=project_date_1.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products_1,
        )
        create_res_1 = await grpc_stub.Create(request)

        products_2 = await self.create_product()
        project_date_2 = datetime.datetime.now()
        project_owner_2 = await sync_to_async(User.objects.create)(username="sih", password="12345")
        request = products_controller_pb2.ProjectRequest(
            name="project 3",
            owner=project_owner_2.id,
            pub_date=project_date_2.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products_2,
        )
        create_res_2 = await grpc_stub.Create(request)

        # Query all Project
        res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "id": create_res_0.id,
                        "name": "project 1",
                        "pubDate": project_date_0,
                        "owner": project_owner_0.id,
                        "products": products_0,
                    },
                    {
                        "id": create_res_1.id,
                        "name": "project 2",
                        "pubDate": project_date_1,
                        "owner": project_owner_1.id,
                        "products": products_1,
                    },
                    {
                        "id": create_res_2.id,
                        "name": "project 3",
                        "pubDate": project_date_2,
                        "owner": project_owner_2.id,
                        "products": products_2,
                    },
                ]
            },
        )

    @freeze_time("2024-02-02 03:21:34")
    async def test_async_partial_update_project(self):
        grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Project Object
        products = await self.create_product()
        project_date = datetime.datetime.now()
        project_owner = await sync_to_async(User.objects.create)(username="k-dot", password="21")
        request = products_controller_pb2.ProjectRequest(
            name="untitled unmastered",
            owner=project_owner.id,
            pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products,
        )
        create_res = await grpc_stub.Create(request)

        # Query one Project Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=create_res.id))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": create_res.id,
                "name": "untitled unmastered",
                "pubDate": project_date,
                "owner": project_owner.id,
                "products": products,
            },
        )

        # Partial Update Project Object in dataset
        new_date = project_date + datetime.timedelta(days=30)
        partial_update_res = await grpc_stub.PartialUpdate(
            products_controller_pb2.ProjectPartialUpdateRequest(
                id=create_res.id,
                _partial_update_fields=["name", "pub_date"],
                name="classic",
                pub_date=new_date.strftime("%Y-%m-%dT%H:%M:%S"),
            )
        )

        # Query one Project Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=partial_update_res.id))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": create_res.id,
                "name": "classic",
                "pubDate": new_date,
                "owner": project_owner.id,
                "products": products,
            },
        )

    @freeze_time("2024-02-02 03:21:34")
    async def test_async_retrieve_project(self):
        grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)

        # Create Project Object
        products_0 = await self.create_product()
        project_date_0 = datetime.datetime.now()
        project_owner_0 = await sync_to_async(User.objects.create)(username="thermal", password="12345")
        request = products_controller_pb2.ProjectRequest(
            name="temp",
            owner=project_owner_0.id,
            pub_date=project_date_0.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products_0,
        )
        await grpc_stub.Create(request)

        products_1 = await self.create_product()
        project_date_1 = datetime.datetime.now()
        project_owner_1 = await sync_to_async(User.objects.create)(username="radar", password="12345")
        request = products_controller_pb2.ProjectRequest(
            name="3d",
            owner=project_owner_1.id,
            pub_date=project_date_1.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products_1,
        )
        await grpc_stub.Create(request)

        products_2 = await self.create_product()
        project_date_2 = datetime.datetime.now()
        project_owner_2 = await sync_to_async(User.objects.create)(username="lidar", password="12345")
        request = products_controller_pb2.ProjectRequest(
            name="3d but light",
            owner=project_owner_2.id,
            pub_date=project_date_2.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products_2,
        )
        create_res = await grpc_stub.Create(request)

        # Query one Project Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=create_res.id))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": create_res.id,
                "name": "3d but light",
                "pubDate": project_date_2,
                "owner": project_owner_2.id,
                "products": products_2,
            },
        )

    @freeze_time("2024-02-02 03:21:34")
    async def test_async_update_project(self):
        grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Project Object
        products = await self.create_product()
        project_date = datetime.datetime.now()
        project_owner = await sync_to_async(User.objects.create)(username="jpegmafia X danny brown", password="21")
        request = products_controller_pb2.ProjectRequest(
            name="awesome album",
            owner=project_owner.id,
            pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
            products=products,
        )
        create_res = await grpc_stub.Create(request)

        # Query one Project Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=create_res.id))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": create_res.id,
                "name": "awesome album",
                "pubDate": project_date,
                "owner": project_owner.id,
                "products": products,
            },
        )

        # Partial Update Project Object in dataset
        new_date = project_date + datetime.timedelta(days=3)
        update_res = await grpc_stub.Update(
            products_controller_pb2.ProjectRequest(
                id=create_res.id,
                name="classic",
                owner=project_owner.id,
                pub_date=new_date.strftime("%Y-%m-%dT%H:%M:%S"),
                products=products,
            )
        )

        # Query one Project Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=update_res.id))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": create_res.id,
                "name": "classic",
                "pubDate": new_date,
                "owner": project_owner.id,
                "products": products,
            },
        )
