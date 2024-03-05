from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC
from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc
from features.products_controller.views.category import CategoryService
from features.products_controller.views.products.coffee_machine import CoffeeMachineService
from google.protobuf import json_format


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestCoffeeMachine(TransactionTestCase):
    reset_sequences = True
    """
    gRPC use proto3 that doesn't distinguish 0 and null so the return message will not be serialized with the null values.
    If one value is 0, it will not be in the Response.
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
        self.coffee_machine_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_CoffeeMachineControllerServicer_to_server,
            CoffeeMachineService.as_servicer(),
        )

    def tearDown(self):
        self.category_fake_grpc.close()
        self.coffee_machine_fake_grpc.close()

    async def create_category(self, name: str = "category") -> int:
        category_grpc_stub = self.category_fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)
        request = products_controller_pb2.CategoryRequest(name=name)
        category = await category_grpc_stub.Create(request)
        return category.id

    async def test_async_create_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category & LedMode Object
        category_id = await self.create_category()

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
            categories=[category_id],
        )
        await grpc_stub.Create(request)

        # Check one CoffeeMachine dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "categories": [str(category_id)],
                        "id": 1,
                        "name": "cofeee",
                        "status": 1,
                        "heat": 110.01,
                        "waterLevel": 1,
                        "usedWaterLevel": 2,
                        "coffeeLevel": 1,
                        "filterPosition": True,
                        "modeValue": 1,
                    }
                ]
            },
        )

    async def test_async_destroy_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Create Category & LedMode Object
        category_id = await self.create_category()

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
            categories=[category_id],
        )
        await grpc_stub.Create(request)

        # Check one CoffeeMachine Object in dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "categories": [str(category_id)],
                        "id": 1,
                        "name": "kill coffee",
                        "status": 1,
                        "heat": 90.0,
                        "waterLevel": 1,
                        "coffeeLevel": 1,
                        "filterPosition": True,
                    }
                ]
            },
        )

        # Delete CoffeeMachine Object
        request = products_controller_pb2.CoffeeMachineDestroyRequest(id=json_res["results"][0]["id"])
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertListEqual(list(res.results), [])

    async def test_async_list_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Create Category & LedMode Object
        category_id_1 = await self.create_category("1")
        category_id_2 = await self.create_category("2")
        category_id_3 = await self.create_category("3")

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
            categories=[category_id_1],
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.CoffeeMachineRequest(
            name="kill coffee why not",
            status=2,
            heat=190.0,
            water_level=1,
            used_water_level=0,
            coffee_level=1,
            filter_position=True,
            mode_value=0,
            categories=[category_id_2],
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.CoffeeMachineRequest(
            name="kill",
            status=3,
            heat=80.1,
            water_level=0,
            used_water_level=1,
            coffee_level=1,
            filter_position=True,
            mode_value=1,
            categories=[category_id_3],
        )
        await grpc_stub.Create(request)
        self.maxDiff = None
        # Query all CoffeeMachine
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "categories": [str(category_id_1)],
                        "id": 1,
                        "name": "coffee kitchen",
                        "status": 1,
                        "heat": 91.0,
                        "coffeeLevel": 1,
                        "filterPosition": True,
                        "modeValue": 3,
                    },
                    {
                        "categories": [str(category_id_2)],
                        "id": 2,
                        "name": "kill coffee why not",
                        "status": 2,
                        "heat": 190.0,
                        "waterLevel": 1,
                        "coffeeLevel": 1,
                        "filterPosition": True,
                    },
                    {
                        "categories": [str(category_id_3)],
                        "id": 3,
                        "name": "kill",
                        "status": 3,
                        "heat": 80.1,
                        "usedWaterLevel": 1,
                        "coffeeLevel": 1,
                        "filterPosition": True,
                        "modeValue": 1,
                    },
                ]
            },
        )

    async def test_async_partial_update_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )
        self.maxDiff = None

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category & LedMode Object
        category_id = await self.create_category("nnnna")

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
            categories=[category_id],
        )
        await grpc_stub.Create(request)

        # Check one coffee_machine in dataset
        res = await grpc_stub.List(products_controller_pb2.CoffeeMachineListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "id": 1,
                        "name": "love coffee",
                        "status": 2,
                        "heat": 40.16,
                        "waterLevel": 1,
                        "coffeeLevel": 1,
                        "filterPosition": True,
                        "categories": [str(category_id)],
                    }
                ]
            },
        )

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": 1,
                "name": "love coffee",
                "status": 2,
                "heat": 40.16,
                "waterLevel": 1,
                "coffeeLevel": 1,
                "filterPosition": True,
                "categories": [str(category_id)],
            },
        )

        # Partial Update CoffeeMachine Object in dataset
        res = await grpc_stub.PartialUpdate(
            products_controller_pb2.CoffeeMachinePartialUpdateRequest(
                id=1, _partial_update_fields=["name", "heat"], name="wow", heat=0.55
            )
        )

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": 1,
                "name": "wow",
                "status": 2,
                "heat": 0.55,
                "waterLevel": 1,
                "coffeeLevel": 1,
                "filterPosition": True,
                "categories": [str(category_id)],
            },
        )

    async def test_async_retrieve_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Create Category & LedMode Object
        category_id_1 = await self.create_category("11")
        category_id_2 = await self.create_category("21")
        category_id_3 = await self.create_category("13")

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
            categories=[category_id_1],
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
            categories=[category_id_2],
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
            categories=[category_id_3],
        )
        await grpc_stub.Create(request)

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=3))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": 3,
                "name": "no more coffee",
                "status": 3,
                "categories": [str(category_id_3)],
            },
        )

    async def test_async_update_coffee_machine(self):
        grpc_stub = self.coffee_machine_fake_grpc.get_fake_stub(
            products_controller_pb2_grpc.CoffeeMachineControllerStub
        )

        # Create Category & LedMode Object
        category_id = await self.create_category("222")

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
            categories=[category_id],
        )
        await grpc_stub.Create(request)

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": 1,
                "name": "killer of tha coffee",
                "status": 3,
                "heat": 60.3,
                "waterLevel": 2,
                "usedWaterLevel": 2,
                "coffeeLevel": 2,
                "filterPosition": True,
                "modeValue": 2,
                "categories": [str(category_id)],
            },
        )

        # Query one Update Object in dataset
        res = await grpc_stub.Update(
            products_controller_pb2.CoffeeMachineRequest(
                id=1,
                name="killer of tha coffee",
                status=1,
                heat=90.0,
                water_level=2,
                used_water_level=2,
                coffee_level=1,
                filter_position=False,
                mode_value=2,
                categories=[category_id],
            )
        )

        # Query one CoffeeMachine Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CoffeeMachineRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "id": 1,
                "name": "killer of tha coffee",
                "status": 1,
                "heat": 90.0,
                "waterLevel": 2,
                "usedWaterLevel": 2,
                "coffeeLevel": 1,
                "modeValue": 2,
                "categories": [str(category_id)],
            },
        )
