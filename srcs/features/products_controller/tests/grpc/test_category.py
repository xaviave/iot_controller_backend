from django.test import TransactionTestCase, override_settings
from django_socio_grpc.tests.grpc_test_utils.fake_grpc import FakeFullAIOGRPC
from features.products_controller.grpc import (
    products_controller_pb2,
    products_controller_pb2_grpc,
)
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
        create_res = await grpc_stub.Create(request)

        # Check one category in dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"results": [{"id": create_res.id, "name": "tom"}]})

    async def test_async_destroy_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Object
        request = products_controller_pb2.CategoryRequest(name="kill me")
        create_res = await grpc_stub.Create(request)

        # Check one Category Object in dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"results": [{"id": create_res.id, "name": "kill me"}]})

        # Delete Category Object
        request = products_controller_pb2.CategoryDestroyRequest(id=create_res.id)
        grpc_stub.Destroy(request)

        # Check empty dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        self.assertListEqual(list(res.results), [])

    async def test_async_list_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Objects
        request = products_controller_pb2.CategoryRequest(name="person_1")
        create_res_0 = await grpc_stub.Create(request)
        request = products_controller_pb2.CategoryRequest(name="person_2")
        create_res_1 = await grpc_stub.Create(request)
        request = products_controller_pb2.CategoryRequest(name="person_3")
        create_res_2 = await grpc_stub.Create(request)

        # Check three Category Objects in dataset
        res = await grpc_stub.List(products_controller_pb2.CategoryListRequest())
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(
            json_res,
            {
                "results": [
                    {"id": create_res_0.id, "name": "person_1"},
                    {"id": create_res_1.id, "name": "person_2"},
                    {"id": create_res_2.id, "name": "person_3"},
                ]
            },
        )

    async def test_async_partial_update_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Objects
        request = products_controller_pb2.CategoryRequest(name="person_6")
        create_res = await grpc_stub.Create(request)

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=create_res.id))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": create_res.id, "name": "person_6"})

        # Query one Partial Update Object in dataset
        partial_update_res = await grpc_stub.PartialUpdate(
            products_controller_pb2.CategoryPartialUpdateRequest(
                id=create_res.id, _partial_update_fields=["name"], name="wow"
            )
        )

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=partial_update_res.id))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": create_res.id, "name": "wow"})

    async def test_async_retrieve_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create two Category Object
        request = products_controller_pb2.CategoryRequest(name="don't pick me")
        await grpc_stub.Create(request)
        request = products_controller_pb2.CategoryRequest(name="pick me")
        create_res = await grpc_stub.Create(request)

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=create_res.id))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": create_res.id, "name": "pick me"})

    async def test_async_update_category(self):
        grpc_stub = self.fake_grpc.get_fake_stub(products_controller_pb2_grpc.CategoryControllerStub)

        # Create Category Objects
        request = products_controller_pb2.CategoryRequest(name="sisi")
        create_res = await grpc_stub.Create(request)

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=create_res.id))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": create_res.id, "name": "sisi"})

        # Query one Update Object in dataset
        update_res = await grpc_stub.Update(products_controller_pb2.CategoryRequest(id=create_res.id, name="up"))

        # Query one Category Object in dataset
        res = await grpc_stub.Retrieve(products_controller_pb2.CategoryRetrieveRequest(id=update_res.id))
        json_res = json_format.MessageToDict(res)
        self.assertDictEqual(json_res, {"id": create_res.id, "name": "up"})
