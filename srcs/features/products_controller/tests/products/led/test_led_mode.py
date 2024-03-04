from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC
from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc
from features.products_controller.views.products.led.led_mode import LedModeService
from google.protobuf import json_format


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestLedMode(TransactionTestCase):
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
        self.fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_LedModeControllerServicer_to_server,
            LedModeService.as_servicer(),
        )

    def tearDown(self):
        self.fake_grpc.close()

    async def test_async_create_led_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.LedModeListRequest())
        self.assertListEqual(list(res.results), [])

        # Create LedMode Object
        request = products_controller_pb2.LedModeRequest(name="tom")
        await grpc_stub.Create(request)

        # Check one led_mode in dataset
        res = await grpc_stub.List(products_controller_pb2.LedModeListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(json_res, {"results": [{"id": 1, "name": "tom"}]})

    async def test_async_destroy_led_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)

        # Create LedMode Object
        request = products_controller_pb2.LedModeRequest(name="kill me")
        await grpc_stub.Create(request)

        # Check one LedMode Object in dataset
        res = await grpc_stub.List(products_controller_pb2.LedModeListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(json_res, {"results": [{"id": 1, "name": "kill me"}]})

        # Delete LedMode Object
        request = products_controller_pb2.LedModeDestroyRequest(id=json_res["results"][0]["id"])
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.LedModeListRequest())
        self.assertListEqual(list(res.results), [])

    async def test_async_list_led_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)

        # Create LedMode Objects
        request = products_controller_pb2.LedModeRequest(name="person_1")
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedModeRequest(name="person_2")
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedModeRequest(name="person_3")
        await grpc_stub.Create(request)

        # Check three LedMode Objects in dataset
        res = await grpc_stub.List(products_controller_pb2.LedModeListRequest())
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(
            json_res,
            {"results": [{"id": 1, "name": "person_1"}, {"id": 2, "name": "person_2"}, {"id": 3, "name": "person_3"}]},
        )

    async def test_async_partial_update_led_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)

        # Create LedMode Objects
        request = products_controller_pb2.LedModeRequest(name="person_6")
        await grpc_stub.Create(request)

        # Query one LedMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedModeRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(json_res, {"id": 1, "name": "person_6"})

        # Query one Partial Update Object in dataset
        res = await grpc_stub.PartialUpdate(
            products_controller_pb2.LedModePartialUpdateRequest(id=1, _partial_update_fields=["name"], name="wow")
        )

        # Query one LedMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedModeRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(json_res, {"id": 1, "name": "wow"})

    async def test_async_retrieve_led_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)

        # Create two LedMode Object
        request = products_controller_pb2.LedModeRequest(name="don't pick me")
        await grpc_stub.Create(request)
        request = products_controller_pb2.LedModeRequest(name="pick me")
        await grpc_stub.Create(request)

        # Query one LedMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedModeRetrieveRequest(id=2))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(json_res, {"id": 2, "name": "pick me"})

    async def test_async_update_led_mode(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.LedModeControllerStub)

        # Create LedMode Objects
        request = products_controller_pb2.LedModeRequest(name="sisi")
        await grpc_stub.Create(request)

        # Query one LedMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedModeRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(json_res, {"id": 1, "name": "sisi"})

        # Query one Update Object in dataset
        res = await grpc_stub.Update(products_controller_pb2.LedModeRequest(id=1, name="up"))

        # Query one LedMode Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.LedModeRetrieveRequest(id=1))
        json_res = self.clean_response(json_format.MessageToDict(res))
        self.assertDictEqual(json_res, {"id": 1, "name": "up"})
