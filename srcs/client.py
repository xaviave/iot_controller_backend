import asyncio
import logging

import grpc
from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = products_controller_pb2_grpc.ProjectControllerStub(channel)
        # request = products_controller_pb2.ProjectRequest(name="tom")
        # response = stub.Create(request)
        # print(response.__dict__)
        print("----- List -----")
        res = await stub.List(products_controller_pb2.ProjectListRequest())
        for c in res.results:
            for p in c.products:
                print(f"{p=}")
                print(p.WhichOneof("product"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
