from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC
from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc
from features.products_controller.views.category import CategoryService
from google.protobuf import json_format


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestCategory(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        self.fake_grpc = FakeFullAIOGRPC(
            products_controller_pb2_grpc.add_CategoryControllerServicer_to_server,
            CategoryService.as_servicer(),
        )

    def tearDown(self):
        self.fake_grpc.close()

    async def test_async_create_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        self.assertListEqual(list(res.results), [])

        # Create Category Object
        request = products_controller_pb2.CategoryRequest(name="tom")
        await grpc_stub.Create(request)

        # Check one category in dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"results": [{"id": 1, "name": "tom"}]})

    async def test_async_destroy_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Object
        request = products_controller_pb2.CategoryRequest(name="kill me")
        await grpc_stub.Create(request)

        # Check one Category Object in dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"results": [{"id": 1, "name": "kill me"}]})

        # Delete Category Object
        request = products_controller_pb2.CategoryDestroyRequest(id=json_res["results"][0]["id"])
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        self.assertListEqual(list(res.results), [])

    async def test_async_list_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Objects
        request = products_controller_pb2.CategoryRequest(name="person_1")
        await grpc_stub.Create(request)
        request = products_controller_pb2.CategoryRequest(name="person_2")
        await grpc_stub.Create(request)
        request = products_controller_pb2.CategoryRequest(name="person_3")
        await grpc_stub.Create(request)

        # Check three Category Objects in dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(
            json_res,
            {"results": [{"id": 1, "name": "person_1"}, {"id": 2, "name": "person_2"}, {"id": 3, "name": "person_3"}]},
        )

    async def test_async_partial_update_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Objects
        request = products_controller_pb2.CategoryRequest(name="person_6")
        await grpc_stub.Create(request)

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=1))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": 1, "name": "person_6"})

        # Query one Partial Update Object in dataset
        res = await grpc_stub.PartialUpdate(
            products_controller_pb2.CategoryPartialUpdateRequest(id=1, _partial_update_fields=["name"], name="wow")
        )

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=1))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": 1, "name": "wow"})

    async def test_async_retrieve_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create two Category Object
        request = products_controller_pb2.CategoryRequest(name="don't pick me")
        await grpc_stub.Create(request)
        request = products_controller_pb2.CategoryRequest(name="pick me")
        await grpc_stub.Create(request)

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=2))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": 2, "name": "pick me"})

    async def test_async_update_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Objects
        request = products_controller_pb2.CategoryRequest(name="sisi")
        await grpc_stub.Create(request)

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=1))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": 1, "name": "sisi"})

        # Query one Update Object in dataset
        res = await grpc_stub.Update(products_controller_pb2.CategoryRequest(id=1, name="up"))

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=1))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": 1, "name": "up"})
