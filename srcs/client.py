# ruff: noqa: S106, S104, S311

import asyncio
import logging
import random
import string
from datetime import datetime

import grpc
from google.protobuf import struct_pb2

from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc

# Create Category Object
category_request = products_controller_pb2.CategoryRequest(name="cate")
category_response = products_controller_pb2.CategoryResponse(name="cate")

# Create CoffeeMachine Object
coffee_machine_args = {
    "name": "".join(random.choice(string.ascii_lowercase) for _ in range(20)),
    "status": 1,
    "heat": 110.01,
    "water_level": 1,
    "used_water_level": 2,
    "coffee_level": 1,
    "filter_position": True,
    "mode_value": 1,
    "categories": [category_request],
    "ip_address": "0.0.0.0",
}
coffee_machine_request = products_controller_pb2.CoffeeMachineRequest(**coffee_machine_args)
coffee_machine_args["categories"] = [category_response]
coffee_machine_response = products_controller_pb2.CoffeeMachineResponse(**coffee_machine_args)

# Create LedMode Object
color_mode_request = products_controller_pb2.ColorModeRequest(name="color_mode", color="#1234df")
color_mode_response = products_controller_pb2.ColorModeResponse(name="color_mode", color="#1234df")

led_mode_request = products_controller_pb2.LedModeRequest()
led_mode_request.ColorMode.CopyFrom(color_mode_request)
led_mode_response = products_controller_pb2.LedModeResponse()
led_mode_response.ColorMode.CopyFrom(color_mode_response)

# Create LedPanel Object
led_panel_args = {
    "name": "".join(random.choice(string.ascii_lowercase) for _ in range(20)),
    "status": 3,
    "brightness": 0.05,
    "mode": led_mode_request,
    "categories": [category_request],
    "ip_address": "0.0.0.0",
}

led_panel_request = products_controller_pb2.LedPanelRequest(**led_panel_args)
led_panel_args["mode"] = led_mode_response
led_panel_args["categories"] = [category_response]
led_panel_response = products_controller_pb2.LedPanelResponse(**led_panel_args)

base_product_1_request = products_controller_pb2.BaseProductRequest()
base_product_1_request.CoffeeMachine.CopyFrom(coffee_machine_request)
base_product_1_response = products_controller_pb2.BaseProductResponse()
base_product_1_response.CoffeeMachine.CopyFrom(coffee_machine_response)

base_product_2_request = products_controller_pb2.BaseProductRequest()
base_product_2_request.LedPanel.CopyFrom(led_panel_request)
base_product_2_response = products_controller_pb2.BaseProductResponse()
base_product_2_response.LedPanel.CopyFrom(led_panel_response)

owner_request = products_controller_pb2.UserRequest(username="gmx")
project_date = datetime.now()

request = products_controller_pb2.ProjectRequest(
    name="project smth",
    owner=owner_request,
    pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
    products=[base_product_1_request, base_product_2_request],
)

# response = products_controller_pb2.ProjectResponse(
#     id=1,
#     name="project smth",
#     owner=owner_request,
#     pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
#     products=[base_product_1_response, base_product_2_response],
# )

"""
Project filter/search/order
"""
# filter_as_dict = {"ordering": "-pub_date"}
# filter_as_dict = {"search": "gmx", "ordering": "-pub_date"}
# filter_as_dict = {"name": "project no filter", "ordering": "-pub_date"}
# filter_as_dict = {"search": "gmx", "name": "project no filter", "ordering": "-pub_date"}

"""
Product filter/search/order
"""
filter_as_dict = {"search": "cat"}
filter_as_struct = struct_pb2.Struct()
filter_as_struct.update(filter_as_dict)

# Getting the 11 to 20 elements following backend ordering
pagination_as_dict = {"page": 2, "page_size": 6}
pagination_as_struct = struct_pb2.Struct()
pagination_as_struct.update(pagination_as_dict)


async def main():
    async with grpc.aio.insecure_channel("grpc_server:50053") as channel:
        products_controller_pb2_grpc.ProjectControllerStub(channel)
        stub_product = products_controller_pb2_grpc.LedPanelControllerStub(channel)
        # response_stub = stub.Create(request)
        # print(await response_stub)
        # print("----- List Project -----")
        # res = await stub_project.List(products_controller_pb2.ProjectListRequest(_filters=filter_as_struct))
        # for c in res.results:
        #     print(c)
        #     # for p in c.products:
        #     #     print(f"{p=}")
        #     #     print(p.WhichOneof("product"))

        print("----- List Product -----")
        res = await stub_product.List(
            products_controller_pb2.LedPanelListRequest(_filters=filter_as_struct, _pagination=pagination_as_struct)
        )
        for c in res.results:
            print(f"\n{c=}{'-' * 100}")
            # for p in c.products:
            #     print(f"{p=}")
            #     print(p.WhichOneof("product"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
