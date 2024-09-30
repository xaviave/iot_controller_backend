from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC

from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc
from features.products_controller.services.products.led.led_mode import PatternModeService


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestPatternMode(TransactionTestCase):
    def setUp(self) -> None:
        self.fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_PatternModeControllerServicer_to_server,
            PatternModeService.as_servicer(),
        )

    def tearDown(self) -> None:
        self.fake_grpc.close()

    async def test_async_create_color_mode(self) -> None:
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.PatternModeControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.PatternModeListRequest())
        assert list(res.results) == []

        # Create PatternMode Object
        request = products_controller_pb2.PatternModeRequest(name="tom", fps=12.1, blink=0, palette=["#000000"])
        create_res = await grpc_stub.Create(request)

        # Check one color_mode in dataset
        res = await grpc_stub.List(products_controller_pb2.PatternModeListRequest())
        assert res.results == [create_res]

    async def test_async_destroy_color_mode(self) -> None:
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.PatternModeControllerStub)

        # Create PatternMode Object
        request = products_controller_pb2.PatternModeRequest(name="kill me", fps=2, blink=0.9, palette=["#000000"])
        create_res = await grpc_stub.Create(request)

        # Check one PatternMode Object in dataset
        res = await grpc_stub.List(products_controller_pb2.PatternModeListRequest())
        assert res.results == [create_res]

        # Delete PatternMode Object
        request = products_controller_pb2.PatternModeDestroyRequest(id=create_res.id)
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.PatternModeListRequest())
        assert list(res.results) == []

    async def test_async_list_color_mode(self) -> None:
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.PatternModeControllerStub)

        # Create PatternMode Objects
        request = products_controller_pb2.PatternModeRequest(name="person_1", fps=12, blink=2, palette=["#000000"])
        create_res_0 = await grpc_stub.Create(request)
        request = products_controller_pb2.PatternModeRequest(name="person_2", fps=12, blink=2, palette=["#000000"])
        create_res_1 = await grpc_stub.Create(request)
        request = products_controller_pb2.PatternModeRequest(name="person_3", fps=12, blink=2, palette=["#000000"])
        create_res_2 = await grpc_stub.Create(request)

        # Check three PatternMode Objects in dataset
        res = await grpc_stub.List(products_controller_pb2.PatternModeListRequest())
        assert res.results == [create_res_0, create_res_1, create_res_2]

    async def test_async_partial_update_color_mode(self) -> None:
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.PatternModeControllerStub)

        # Create PatternMode Objects
        request = products_controller_pb2.PatternModeRequest(name="person_6", fps=12, blink=2, palette=["#000000"])
        create_res = await grpc_stub.Create(request)

        # Query one PatternMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.PatternModeRetrieveRequest(id=create_res.id))
        assert res == create_res

        # Query one Partial Update Object in dataset
        partial_update_res = await grpc_stub.PartialUpdate(
            products_controller_pb2.PatternModePartialUpdateRequest(
                id=create_res.id, _partial_update_fields=["name"], name="wow"
            )
        )

        # Query one PatternMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.PatternModeRetrieveRequest(id=partial_update_res.id))
        assert res == partial_update_res

    async def test_async_retrieve_color_mode(self) -> None:
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.PatternModeControllerStub)

        # Create two PatternMode Object
        request = products_controller_pb2.PatternModeRequest(name="don't pick me", fps=12, blink=2, palette=["#000000"])
        await grpc_stub.Create(request)
        request = products_controller_pb2.PatternModeRequest(name="pick me", fps=12, blink=21, palette=["#000000"])
        create_res = await grpc_stub.Create(request)

        # Query one PatternMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.PatternModeRetrieveRequest(id=create_res.id))
        assert res == create_res

    async def test_async_update_color_mode(self) -> None:
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.PatternModeControllerStub)

        # Create PatternMode Objects
        request = products_controller_pb2.PatternModeRequest(name="sisi", fps=1, blink=22, palette=["#000000"])
        create_res = await grpc_stub.Create(request)

        # Query one PatternMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.PatternModeRetrieveRequest(id=create_res.id))
        assert res == create_res

        # Query one Update Object in dataset
        update_res = await grpc_stub.Update(
            products_controller_pb2.PatternModeRequest(
                id=create_res.id, name="up", fps=120, blink=20, palette=["#000000"]
            )
        )

        # Query one PatternMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.PatternModeRetrieveRequest(id=update_res.id))
        assert res == update_res
