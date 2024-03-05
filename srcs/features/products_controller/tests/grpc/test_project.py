import datetime

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

    def _clean_dict_response(self, d: dict) -> dict:
        return {k: v for k, v in d.items() if k not in self._ignored_key}

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
        request = products_controller_pb2.CategoryRequest(name="led or smth")
        category = await category_grpc_stub.Create(request)

        # Create LedMode Object
        led_mode_grpc_stub = self.led_mode_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)
        request = products_controller_pb2.LedModeRequest(name="flash flash")
        led_mode = await led_mode_grpc_stub.Create(request)

        # Create CoffeeMachine Object
        coffee_machine_grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )
        request = products_controller_pb2.CoffeeMachineRequest(
            name="coffee",
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
            name="bedroom home", status=3, brightness=0.05, mode=led_mode.id, categories=[category.id]
        )
        led_panel = await led_panel_grpc_stub.Create(request)
        return [coffee_machine.uuid, led_panel.uuid]

    @freeze_time("2012-01-14 03:21:34")
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
                        "pubDate": project_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "owner": project_owner.id,
                        "products": products,
                    }
                ]
            },
        )

    # async def test_async_destroy_project(self):
    #     grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)
    #
    #     # Create Project Object
    #     request = products_controller_pb2.ProjectRequest(
    #         name="kill project",
    #     )
    #     await grpc_stub.Create(request)
    #
    #     # Check one Project Object in dataset
    #     res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
    #     json_res = self.clean_response(json_format.MessageToDict(res))
    #     self.assertDictEqual(
    #         json_res,
    #         {
    #             "results": [
    #                 {
    #                     "id": 1,
    #                     "name": "kill project",
    #                 }
    #             ]
    #         },
    #     )
    #
    #     # Delete Project Object
    #     request = products_controller_pb2.ProjectDestroyRequest(id=json_res["results"][0]["id"])
    #     grpc_stub.Destroy(request)
    #
    #     # Check empty dataset
    #     res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
    #     self.assertListEqual(list(res.results), [])
    #
    # async def test_async_list_project(self):
    #     grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)
    #
    #     # Create Project Object
    #     request = products_controller_pb2.ProjectRequest(
    #         name="project kitchen",
    #     )
    #     await grpc_stub.Create(request)
    #     request = products_controller_pb2.ProjectRequest(
    #         name="kill project why not",
    #     )
    #     await grpc_stub.Create(request)
    #     request = products_controller_pb2.ProjectRequest(
    #         name="kill",
    #     )
    #     await grpc_stub.Create(request)
    #     self.maxDiff = None
    #     # Query all Project
    #     res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
    #     json_res = self.clean_response(json_format.MessageToDict(res))
    #     self.assertDictEqual(
    #         json_res,
    #         {
    #             "results": [
    #                 {
    #                     "id": 1,
    #                     "name": "project kitchen",
    #                 },
    #                 {
    #                     "id": 2,
    #                     "name": "kill project why not",
    #                 },
    #                 {
    #                     "id": 3,
    #                     "name": "kill",
    #                 },
    #             ]
    #         },
    #     )
    #
    # async def test_async_partial_update_project(self):
    #     grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)
    #     self.maxDiff = None
    #
    #     # Check empty dataset
    #     res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
    #     self.assertListEqual(list(res.results), [])
    #
    #     # Create Project Object
    #     request = products_controller_pb2.ProjectRequest(
    #         name="love project",
    #     )
    #     await grpc_stub.Create(request)
    #
    #     # Check one project in dataset
    #     res = await grpc_stub.List(products_controller_pb2.ProjectListRequest())
    #     json_res = self.clean_response(json_format.MessageToDict(res))
    #     self.assertDictEqual(
    #         json_res,
    #         {
    #             "results": [
    #                 {
    #                     "id": 1,
    #                     "name": "love project",
    #                 }
    #             ]
    #         },
    #     )
    #
    #     # Query one Project Object in dataset
    #     res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=1))
    #     json_res = self.clean_response(json_format.MessageToDict(res))
    #     self.assertDictEqual(
    #         json_res,
    #         {
    #             "id": 1,
    #             "name": "love project",
    #         },
    #     )
    #
    #     # Partial Update Project Object in dataset
    #     res = await grpc_stub.PartialUpdate(
    #         products_controller_pb2.ProjectPartialUpdateRequest(
    #             id=1,
    #             _partial_update_fields=["name", "heat"],
    #             name="wow",
    #         )
    #     )
    #
    #     # Query one Project Object in dataset
    #     res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=1))
    #     json_res = self.clean_response(json_format.MessageToDict(res))
    #     self.assertDictEqual(
    #         json_res,
    #         {
    #             "id": 1,
    #             "name": "wow",
    #         },
    #     )
    #
    # async def test_async_retrieve_project(self):
    #     grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)
    #
    #     # Create Project Object
    #     request = products_controller_pb2.ProjectRequest(
    #         name="kill project",
    #     )
    #     await grpc_stub.Create(request)
    #     request = products_controller_pb2.ProjectRequest(
    #         name="kill project 2",
    #     )
    #     await grpc_stub.Create(request)
    #     request = products_controller_pb2.ProjectRequest(
    #         name="no more project",
    #     )
    #     await grpc_stub.Create(request)
    #
    #     # Query one Project Object in dataset
    #     res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=3))
    #     json_res = self.clean_response(json_format.MessageToDict(res))
    #     self.assertDictEqual(
    #         json_res,
    #         {
    #             "id": 3,
    #             "name": "no more project",
    #         },
    #     )
    #
    # async def test_async_update_project(self):
    #     grpc_stub = self.project_fake_grpc.get_fake_stub(products_controller_pb2_grpc.ProjectControllerStub)
    #
    #     # Create Project Object
    #     request = products_controller_pb2.ProjectRequest(
    #         name="killer of tha project",
    #     )
    #     await grpc_stub.Create(request)
    #
    #     # Query one Project Object in dataset
    #     res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=1))
    #     json_res = self.clean_response(json_format.MessageToDict(res))
    #     self.assertDictEqual(
    #         json_res,
    #         {
    #             "id": 1,
    #             "name": "killer of tha project",
    #         },
    #     )
    #
    #     # Query one Update Object in dataset
    #     res = await grpc_stub.Update(
    #         products_controller_pb2.ProjectRequest(
    #             id=1,
    #             name="killer of tha project",
    #         )
    #     )
    #
    #     # Query one Project Object in dataset
    #     res = await grpc_stub.Retrieve(products_controller_pb2.ProjectRetrieveRequest(id=1))
    #     json_res = self.clean_response(json_format.MessageToDict(res))
    #     self.assertDictEqual(
    #         json_res,
    #         {
    #             "id": 1,
    #             "name": "killer of tha project",
    #         },
    #     )
