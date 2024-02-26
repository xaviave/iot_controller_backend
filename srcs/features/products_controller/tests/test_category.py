from django.test import TestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC
from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc
from features.products_controller.views.category import CategoryService
from google.protobuf import json_format


@override_settings(GRPC_FRAMEWORK={"GRPC_ASYNC": True})
class TestCategory(TestCase):
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
        grpc_stub.Create(request)

        # Check one category in dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"results": [{"id": 1, "name": "tom"}]})

    async def test_async_destroy_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Object
        request = products_controller_pb2.CategoryRequest(name="kill me")
        grpc_stub.Create(request)

        # Check one category in dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"results": [{"id": 2, "name": "kill me"}]})

        # Delete Category Object
        request = products_controller_pb2.CategoryDestroyRequest(id=json_res["results"][0]["id"])
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        self.assertListEqual(list(res.results), [])
