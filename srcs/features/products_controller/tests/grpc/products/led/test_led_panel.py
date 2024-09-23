# ruff: noqa: S104

from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC

from features.products_controller.grpc import (
    products_controller_pb2,
    products_controller_pb2_grpc,
)
from features.products_controller.services.category import CategoryService
from features.products_controller.services.products.led.led_mode import ColorModeService
from features.products_controller.services.products.led.led_panel import LedPanelService


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestLedPanel(TransactionTestCase):
    def setUp(self):
        self.category_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_CategoryControllerServicer_to_server,
            CategoryService.as_servicer(),
        )
        self.led_mode_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_ColorModeControllerServicer_to_server,
            ColorModeService.as_servicer(),
        )
        self.led_panel_fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_LedPanelControllerServicer_to_server,
            LedPanelService.as_servicer(),
        )

    def tearDown(self):
        self.category_fake_grpc.close()
        self.led_mode_fake_grpc.close()
        self.led_panel_fake_grpc.close()

    async def create_category(
        self, name: str = "category"
    ) -> (products_controller_pb2.CategoryRequest, products_controller_pb2.CategoryResponse):
        request = products_controller_pb2.CategoryRequest(name=name)
        response = products_controller_pb2.CategoryResponse(name=name)
        return request, response

    async def create_led_mode(
        self, name: str = "led_mode"
    ) -> (products_controller_pb2.LedModeRequest, products_controller_pb2.LedModeResponse):
        request = products_controller_pb2.ColorModeRequest(name=name, color="#1234df")
        response = products_controller_pb2.ColorModeResponse(name=name, color="#1234df")

        led_mode_request = products_controller_pb2.LedModeRequest()
        led_mode_request.ColorMode.CopyFrom(request)
        led_mode_response = products_controller_pb2.LedModeResponse()
        led_mode_response.ColorMode.CopyFrom(response)
        return led_mode_request, led_mode_response

    async def test_async_create_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category & ColorMode Object
        category_request, category_response = await self.create_category()
        led_mode_request, led_mode_response = await self.create_led_mode()

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="home",
            status=1,
            brightness=0.02,
            mode=led_mode_request,
            categories=[category_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Check led_panel in dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertEqual(res.results, [create_res])

    async def test_async_destroy_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Create Category & ColorMode request and response
        # Objects already created before so a query will be done in LedPanelSerializer
        category_request, category_response = await self.create_category()
        led_mode_request, led_mode_response = await self.create_led_mode()

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="kill me",
            status=1,
            brightness=1.22,
            mode=led_mode_request,
            categories=[category_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Check one LedPanel Object in dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertEqual(res.results, [create_res])

        # Delete LedPanel Object
        request = products_controller_pb2.LedPanelDestroyRequest(id=create_res.id)
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertListEqual(list(res.results), [])

    async def test_async_list_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Create Category & ColorMode Object
        category_1_request, category_1_response = await self.create_category("1")
        category_2_request, category_2_response = await self.create_category("2")
        category_3_request, category_3_response = await self.create_category("3")
        led_mode_1_request, led_mode_1_response = await self.create_led_mode("4")
        led_mode_2_request, led_mode_2_response = await self.create_led_mode("5")

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="mamacita",
            status=1,
            brightness=1.08,
            mode=led_mode_1_request,
            categories=[category_1_request],
            ip_address="0.0.0.0",
        )
        create_res_0 = await grpc_stub.Create(request)
        request = products_controller_pb2.LedPanelRequest(
            name="killed me",
            status=3,
            brightness=1.3,
            mode=led_mode_1_request,
            categories=[category_2_request],
            ip_address="0.0.0.0",
        )
        create_res_1 = await grpc_stub.Create(request)
        request = products_controller_pb2.LedPanelRequest(
            name="please past",
            status=2,
            brightness=4.69,
            mode=led_mode_2_request,
            categories=[category_3_request],
            ip_address="0.0.0.0",
        )
        create_res_2 = await grpc_stub.Create(request)

        # Query all LedPanel
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertEqual(res.results, [create_res_0, create_res_1, create_res_2])

    async def test_async_partial_update_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category & ColorMode Object
        category_request, category_response = await self.create_category("nnnna")
        led_mode_request, led_mode_response = await self.create_led_mode("sisi")

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="home, ie",
            status=2,
            brightness=0.99,
            mode=led_mode_request,
            categories=[category_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Check one led_panel in dataset
        res = await grpc_stub.List(products_controller_pb2.LedPanelListRequest())
        self.assertEqual(res.results, [create_res])

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

        # Partial Update LedPanel Object in dataset
        partial_update_res = await grpc_stub.PartialUpdate(
            products_controller_pb2.LedPanelPartialUpdateRequest(
                id=create_res.id,
                _partial_update_fields=["name", "brightness"],
                name="wow",
                brightness=0.55,
            )
        )

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=partial_update_res.id))
        self.assertEqual(res, partial_update_res)

    async def test_async_retrieve_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Create Category & ColorMode Object
        category_1_request, category_1_response = await self.create_category("11")
        category_2_request, category_2_response = await self.create_category("21")
        category_3_request, category_3_response = await self.create_category("13")
        led_mode_1_request, led_mode_1_response = await self.create_led_mode("41")
        led_mode_2_request, led_mode_2_response = await self.create_led_mode("52")

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="mamacita, travis",
            status=1,
            brightness=1.08,
            mode=led_mode_1_request,
            categories=[category_1_request],
            ip_address="0.0.0.0",
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedPanelRequest(
            name="killed me, again",
            status=3,
            brightness=1.3,
            mode=led_mode_2_request,
            categories=[category_2_request],
            ip_address="0.0.0.0",
        )
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedPanelRequest(
            name="please past oh",
            status=2,
            brightness=4.69,
            mode=led_mode_2_request,
            categories=[category_3_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

    async def test_async_update_led_panel(self):
        grpc_stub = self.led_panel_fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedPanelControllerStub)

        # Create Category & ColorMode Object
        category_request, category_response = await self.create_category("222")
        led_mode_request, led_mode_response = await self.create_led_mode("again?")

        # Create LedPanel Object
        request = products_controller_pb2.LedPanelRequest(
            name="no home",
            status=3,
            brightness=0.05,
            mode=led_mode_request,
            categories=[category_request],
            ip_address="0.0.0.0",
        )
        create_res = await grpc_stub.Create(request)

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

        request = products_controller_pb2.LedPanelRequest(
            id=create_res.id,
            ip_address="0.0.0.0",
            name="no hhhome",
            status=2,
            brightness=0.15,
            mode=led_mode_request,
            categories=[category_request],
        )

        # Query one Update Object in dataset
        update_res = await grpc_stub.Update(request)

        # Query one LedPanel Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedPanelRetrieveRequest(id=update_res.id))
        self.assertEqual(res, update_res)
