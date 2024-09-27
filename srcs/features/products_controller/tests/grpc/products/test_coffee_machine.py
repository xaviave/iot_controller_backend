# ruff: noqa: S104

from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC

from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc
from features.products_controller.services.category import CategoryService
from features.products_controller.services.products.coffee_machine import CoffeeMachineService


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestCoffeeMachine(TransactionTestCase):
    def setUp(self):
        self.category_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_CategoryControllerServicer_to_server,
            CategoryService.as_servicer(),
        )
        self.coffee_machine_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_CoffeeMachineControllerServicer_to_server,
            CoffeeMachineService.as_servicer(),
        )

    def tearDown(self):
        self.category_fake_grpc.close()
        self.coffee_machine_fake_grpc.close()

    async def create_category(
        self, name: str = "category"
    ) -> (products_controller_pb2.CategoryRequest, products_controller_pb2.CategoryResponse):
        request = products_controller_pb2.CategoryRequest(name=name)
        response = products_controller_pb2.CategoryResponse(name=name)
        return request, response

    async def test_async_create_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category & LedMode Object
        category_request, category_response = await self.create_category()

        # Create CoffeeMachine Object
        request = products_controller_pb2.CoffeeMachineRequest(
            name="cofeee",
            status=1,
            heat=110.01,
            water_level=1,
            used_water_level=2,
            coffee_level=1,
            filter_position=True,
            mode_value=1,
            categories=[category_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Check one CoffeeMachine dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertEqual(res.results, [create_res])

    async def test_async_destroy_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Create Category & LedMode Object
        category_request, category_response = await self.create_category()

        # Create CoffeeMachine Object
        request = products_controller_pb2.CoffeeMachineRequest(
            name="kill coffee",
            status=1,
            heat=90.0,
            water_level=1,
            used_water_level=0,
            coffee_level=1,
            filter_position=True,
            mode_value=0,
            categories=[category_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Check one CoffeeMachine Object in dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertEqual(res.results, [create_res])

        # Delete CoffeeMachine Object
        request = products_controller_pb2.CoffeeMachineDestroyRequest(id=create_res.id)
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertListEqual(list(res.results), [])

    async def test_async_list_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Create Category & LedMode Object
        category_1_request, category_1_response = await self.create_category("1")
        category_2_request, category_2_response = await self.create_category("2")
        category_3_request, category_3_response = await self.create_category("3")

        # Create CoffeeMachine Object
        request = products_controller_pb2.CoffeeMachineRequest(
            name="coffee kitchen",
            status=1,
            heat=91.0,
            water_level=0,
            used_water_level=0,
            coffee_level=1,
            filter_position=True,
            mode_value=3,
            categories=[category_1_request],
            ip_address="0.0.0.0",
        )
        create_res_0 = await grpc_stub.Create(request)
        request = products_controller_pb2.CoffeeMachineRequest(
            name="kill coffee why not",
            status=2,
            heat=190.0,
            water_level=1,
            used_water_level=0,
            coffee_level=1,
            filter_position=True,
            mode_value=0,
            categories=[category_2_request],
            ip_address="0.0.0.0",
        )
        create_res_1 = await grpc_stub.Create(request)
        request = products_controller_pb2.CoffeeMachineRequest(
            name="kill",
            status=3,
            heat=80.1,
            water_level=0,
            used_water_level=1,
            coffee_level=1,
            filter_position=True,
            mode_value=1,
            categories=[category_3_request],
            ip_address="0.0.0.0",
        )
        create_res_2 = await grpc_stub.Create(request)

        # Query all CoffeeMachine
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertEqual(res.results, [create_res_0, create_res_1, create_res_2])

    async def test_async_partial_update_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category & LedMode Object
        category_request, category_response = await self.create_category("nnnna")

        # Create CoffeeMachine Object
        request = products_controller_pb2.CoffeeMachineRequest(
            name="love coffee",
            status=2,
            heat=40.16,
            water_level=1,
            used_water_level=0,
            coffee_level=1,
            filter_position=True,
            mode_value=0,
            categories=[category_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Check one coffee_machine in dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertEqual(res.results, [create_res])

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

        # Partial Update CoffeeMachine Object in dataset
        partial_create_res = await grpc_stub.PartialUpdate(
            products_controller_pb2.CoffeeMachinePartialUpdateRequest(
                id=create_res.id, _partial_update_fields=["name", "heat"], name="wow", heat=0.55
            )
        )

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=partial_create_res.id))
        self.assertEqual(res, partial_create_res)

    async def test_async_retrieve_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Create Category & LedMode Object
        category_1_request, category_1_response = await self.create_category("11")
        category_2_request, category_2_response = await self.create_category("21")
        category_3_request, category_3_response = await self.create_category("13")

        # Create CoffeeMachine Object
        request = products_controller_pb2.CoffeeMachineRequest(
            name="kill coffee",
            status=1,
            heat=90.0,
            water_level=1,
            used_water_level=0,
            coffee_level=1,
            filter_position=True,
            mode_value=0,
            categories=[category_1_request],
            ip_address="0.0.0.0",
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.CoffeeMachineRequest(
            name="kill coffee 2",
            status=1,
            heat=90.0,
            water_level=1,
            used_water_level=0,
            coffee_level=1,
            filter_position=True,
            mode_value=0,
            categories=[category_2_request],
            ip_address="0.0.0.0",
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.CoffeeMachineRequest(
            name="no more coffee",
            status=3,
            heat=0.0,
            water_level=0,
            used_water_level=0,
            coffee_level=0,
            filter_position=False,
            mode_value=0,
            categories=[category_3_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

    async def test_async_update_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Create Category & LedMode Object
        category_request, category_response = await self.create_category("222")

        # Create CoffeeMachine Object
        request = products_controller_pb2.CoffeeMachineRequest(
            name="killer of tha coffee",
            status=3,
            heat=60.3,
            water_level=2,
            used_water_level=2,
            coffee_level=2,
            filter_position=True,
            mode_value=2,
            categories=[category_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

        # Query one Update Object in dataset
        update_res = await grpc_stub.Update(
            products_controller_pb2.CoffeeMachineRequest(
                id=create_res.id,
                name="killer of tha coffo",
                status=1,
                heat=90.0,
                water_level=2,
                used_water_level=2,
                coffee_level=1,
                filter_position=False,
                mode_value=2,
                categories=[category_request],
                ip_address="0.0.0.0",
            )
        )

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=update_res.id))
        self.assertEqual(res, update_res)
