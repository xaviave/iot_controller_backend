from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC

from features.products_controller.grpc import (
    products_controller_pb2,
    products_controller_pb2_grpc,
)
from features.products_controller.services.products.led.led_mode import ColorModeService


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestColorMode(TransactionTestCase):
    def setUp(self):
        self.fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_ColorModeControllerServicer_to_server,
            ColorModeService.as_servicer(),
        )

    def tearDown(self):
        self.fake_grpc.close()

    async def test_async_create_color_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.ColorModeControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.ColorModeListRequest())
        self.assertEqual(list(res.results), [])

        # Create ColorMode Object
        request = products_controller_pb2.ColorModeRequest(name="tom", color="#949200")
        create_res = await grpc_stub.Create(request)

        # Check one color_mode in dataset
        res = await grpc_stub.List(products_controller_pb2.ColorModeListRequest())
        self.assertEqual(res.results, [create_res])

    async def test_async_destroy_color_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.ColorModeControllerStub)

        # Create ColorMode Object
        request = products_controller_pb2.ColorModeRequest(name="kill me", color="#f3ff00")
        create_res = await grpc_stub.Create(request)

        # Check one ColorMode Object in dataset
        res = await grpc_stub.List(products_controller_pb2.ColorModeListRequest())
        self.assertEqual(res.results, [create_res])

        # Delete ColorMode Object
        request = products_controller_pb2.ColorModeDestroyRequest(id=create_res.id)
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.ColorModeListRequest())
        self.assertEqual(list(res.results), [])

    async def test_async_list_color_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.ColorModeControllerStub)

        # Create ColorMode Objects
        request = products_controller_pb2.ColorModeRequest(name="person_1", color="#111100")
        create_res_0 = await grpc_stub.Create(request)
        request = products_controller_pb2.ColorModeRequest(name="person_2", color="#ff0012")
        create_res_1 = await grpc_stub.Create(request)
        request = products_controller_pb2.ColorModeRequest(name="person_3", color="#ffff00")
        create_res_2 = await grpc_stub.Create(request)

        # Check three ColorMode Objects in dataset
        res = await grpc_stub.List(products_controller_pb2.ColorModeListRequest())
        self.assertEqual(res.results, [create_res_0, create_res_1, create_res_2])

    async def test_async_partial_update_color_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.ColorModeControllerStub)

        # Create ColorMode Objects
        request = products_controller_pb2.ColorModeRequest(name="person_6", color="#fcff00")
        create_res = await grpc_stub.Create(request)

        # Query one ColorMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ColorModeRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

        # Query one Partial Update Object in dataset
        partial_update_res = await grpc_stub.PartialUpdate(
            products_controller_pb2.ColorModePartialUpdateRequest(
                id=create_res.id, _partial_update_fields=["name"], name="wow"
            )
        )

        # Query one ColorMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ColorModeRetrieveRequest(id=partial_update_res.id))
        self.assertEqual(res, partial_update_res)

    async def test_async_retrieve_color_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.ColorModeControllerStub)

        # Create two ColorMode Object
        request = products_controller_pb2.ColorModeRequest(name="don't pick me", color="#aa11cc")
        await grpc_stub.Create(request)
        request = products_controller_pb2.ColorModeRequest(name="pick me", color="#d2d3d4")
        create_res = await grpc_stub.Create(request)

        # Query one ColorMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ColorModeRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

    async def test_async_update_color_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.ColorModeControllerStub)

        # Create ColorMode Objects
        request = products_controller_pb2.ColorModeRequest(name="sisi", color="#ffcc32")
        create_res = await grpc_stub.Create(request)

        # Query one ColorMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ColorModeRetrieveRequest(id=create_res.id))
        self.assertEqual(res, create_res)

        # Query one Update Object in dataset
        update_res = await grpc_stub.Update(
            products_controller_pb2.ColorModeRequest(id=create_res.id, name="up", color="#d1d2ff")
        )

        # Query one ColorMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.ColorModeRetrieveRequest(id=update_res.id))
        self.assertEqual(res, update_res)
