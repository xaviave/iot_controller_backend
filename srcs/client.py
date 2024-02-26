import asyncio

import grpc
from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = products_controller_pb2_grpc.CategoryControllerStub(channel)
        # print("----- Create -----")
        request = products_controller_pb2.CategoryRequest(name="tom")
        response = stub.Create(request)
        print(response.__dict__)
        print("----- List -----")
        res = await stub.List(products_controller_pb2.CategoryListRequest())
        for c in res.results:
            print(c)


if __name__ == "__main__":
    asyncio.run(main())
