import asyncio
import logging

import grpc

from features.products_controller.grpc import test_polymorphism_pb2_grpc, test_polymorphism_pb2


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = test_polymorphism_pb2_grpc.ProjectControllerStub(channel)
        # request = test_polymorphism_pb2.ProjectRequest(name="tom")
        # response = stub.Create(request)
        # print(response.__dict__)
        print("----- List -----")
        res = await stub.List(test_polymorphism_pb2.ProjectListRequest())
        for c in res.results:
            for p in c.products:
                print(f"{p=}")
                print(p.WhichOneof("product"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
