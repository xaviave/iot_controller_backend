from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC
from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc
from features.products_controller.views.category import CategoryService
from features.products_controller.views.products.led.led_mode import LedModeService
from features.products_controller.views.products.led.led_panel import LedPanelService
from google.protobuf import json_format


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestLedPanel(TransactionTestCase):
    reset_sequences = True

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

    def tearDown(self):
        self.category_fake_grpc.close()
        self.led_mode_fake_grpc.close()
        self.led_panel_fake_grpc.close()

    async def create_category(self, name: str = "category") -> int:
        category_grpc_stub = self.category_fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)
        request = products_controller_pb2.CategoryRequest(name=name)
        category = await category_grpc_stub.Create(request)
        return category.id

    async def create_led_mode(self, name: str = "led_mode") -> int:
        led_mode_grpc_stub = self.led_mode_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)
        request = products_controller_pb2.LedModeRequest(name=name)
        led_mode = await led_mode_grpc_stub.Create(request)
        return led_mode.id

    async def test_async_create_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category & LedMode Object
        category_id = await self.create_category()
        led_mode_id = await self.create_led_mode()

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="home", status=1, brightness=0.02, mode=led_mode_id, categories=[category_id]
        )
        await grpc_stub.Create(request)
        # Check one led_panel in dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "brightness": 0.02,
                        "categories": [str(category_id)],
                        "id": 1,
                        "mode": str(led_mode_id),
                        "name": "home",
                        "status": 1,
                    }
                ]
            },
        )

    async def test_async_destroy_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Create Category & LedMode Object
        category_id = await self.create_category()
        led_mode_id = await self.create_led_mode()

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="kill me", status=1, brightness=1.22, mode=led_mode_id, categories=[category_id]
        )
        await grpc_stub.Create(request)

        # Check one LedPanel Object in dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "brightness": 1.22,
                        "categories": [str(category_id)],
                        "id": 1,
                        "mode": str(led_mode_id),
                        "name": "kill me",
                        "status": 1,
                    }
                ]
            },
        )

        # Delete LedPanel Object
        request = products_controller_pb2.LedPanelDestroyRequest(id=json_res["results"][0]["id"])
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertListEqual(list(res.results), [])

    async def test_async_list_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Create Category & LedMode Object
        category_id_1 = await self.create_category("1")
        category_id_2 = await self.create_category("2")
        category_id_3 = await self.create_category("3")
        led_mode_id_1 = await self.create_led_mode("4")
        led_mode_id_2 = await self.create_led_mode("5")

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="mamacita", status=1, brightness=1.08, mode=led_mode_id_1, categories=[category_id_1]
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedPanelRequest(
            name="killed me", status=3, brightness=1.3, mode=led_mode_id_2, categories=[category_id_2]
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedPanelRequest(
            name="please past", status=2, brightness=4.69, mode=led_mode_id_2, categories=[category_id_3]
        )
        await grpc_stub.Create(request)

        # Query all LedPanel
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "brightness": 1.08,
                        "categories": [str(category_id_1)],
                        "id": 1,
                        "mode": str(led_mode_id_1),
                        "name": "mamacita",
                        "status": 1,
                    },
                    {
                        "brightness": 1.3,
                        "categories": [str(category_id_2)],
                        "id": 2,
                        "mode": str(led_mode_id_2),
                        "name": "killed me",
                        "status": 3,
                    },
                    {
                        "brightness": 4.69,
                        "categories": [str(category_id_3)],
                        "id": 3,
                        "mode": str(led_mode_id_2),
                        "name": "please past",
                        "status": 2,
                    },
                ]
            },
        )

    async def test_async_partial_update_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category & LedMode Object
        category_id = await self.create_category("nnnna")
        led_mode_id = await self.create_led_mode("sisi")

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="home, ie", status=2, brightness=0.99, mode=led_mode_id, categories=[category_id]
        )
        await grpc_stub.Create(request)

        # Check one led_panel in dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {
                        "brightness": 0.99,
                        "categories": [str(category_id)],
                        "id": 1,
                        "mode": str(led_mode_id),
                        "name": "home, ie",
                        "status": 2,
                    }
                ]
            },
        )

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(json_res, {
                        "brightness": 0.99,
                        "categories": [str(category_id)],
                        "id": 1,
                        "mode": str(led_mode_id),
                        "name": "home, ie",
                        "status": 2,
                    })

        # Partial Update LedPanel Object in dataset
        res = await grpc_stub.PartialUpdate(
            products_controller_pb2.LedPanelPartialUpdateRequest(
                id=1, _partial_update_fields=["name", "brightness"], name="wow", brightness=0.55
            )
        )

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "brightness": 0.55,
                "categories": [str(category_id)],
                "id": 1,
                "mode": str(led_mode_id),
                "name": "wow",
                "status": 2,
            },
        )

    async def test_async_retrieve_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Create Category & LedMode Object
        category_id_1 = await self.create_category("11")
        category_id_2 = await self.create_category("21")
        category_id_3 = await self.create_category("13")
        led_mode_id_1 = await self.create_led_mode("41")
        led_mode_id_2 = await self.create_led_mode("52")

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="mamacita, travis", status=1, brightness=1.08, mode=led_mode_id_1, categories=[category_id_1]
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedPanelRequest(
            name="killed me, again", status=3, brightness=1.3, mode=led_mode_id_2, categories=[category_id_2]
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedPanelRequest(
            name="please past oh", status=2, brightness=4.69, mode=led_mode_id_2, categories=[category_id_3]
        )
        await grpc_stub.Create(request)

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=3))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "brightness": 4.69,
                "categories": [str(category_id_3)],
                "id": 3,
                "mode": str(led_mode_id_2),
                "name": "please past oh",
                "status": 2,
            },
        )

    async def test_async_update_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Create Category & LedMode Object
        category_id = await self.create_category("222")
        led_mode_id = await self.create_led_mode("again?")

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="no home", status=3, brightness=0.05, mode=led_mode_id, categories=[category_id]
        )
        await grpc_stub.Create(request)

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "brightness": 0.05,
                "categories": [str(category_id)],
                "id": 1,
                "mode": str(led_mode_id),
                "name": "no home",
                "status": 3,
            },
        )

        # Query one Update Object in dataset
        res = await grpc_stub.Update(
            products_controller_pb2.LedPanelRequest(
                id=1, name="no hhhome", status=2, brightness=0.15, mode=led_mode_id, categories=[category_id]
            )
        )

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {
                "brightness": 0.15,
                "categories": [str(category_id)],
                "id": 1,
                "mode": str(led_mode_id),
                "name": "no hhhome",
                "status": 2,
            },
        )
