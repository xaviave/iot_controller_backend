import asyncio
import logging
from datetime import datetime

import grpc
from features.products_controller.grpc import (
    products_controller_pb2,
    products_controller_pb2_grpc,
)

# Create Category Object
category_request = products_controller_pb2.CategoryRequest(id=1, name="cate")
category_response = products_controller_pb2.CategoryResponse(id=1, name="cate")

# Create LedMode Object
request = products_controller_pb2.ColorModeRequest(name="xavou", color="#1234df")
response = products_controller_pb2.ColorModeResponse(name="xavou", color="#1234df")
led_mode_request = products_controller_pb2.LedModeRequest()
led_mode_request.ColorMode.CopyFrom(request)
led_mode_response = products_controller_pb2.LedModeResponse()
led_mode_response.ColorMode.CopyFrom(response)

# Create CoffeeMachine Object
coffee_machine_args = {
    "id": 1,
    "name": "aoui",
    "status": 1,
    "heat": 110.01,
    "water_level": 1,
    "used_water_level": 2,
    "coffee_level": 1,
    "filter_position": True,
    "mode_value": 1,
    "categories": [category_request],
}
coffee_machine_request = products_controller_pb2.CoffeeMachineRequest(**coffee_machine_args)
coffee_machine_args["categories"] = [category_response]
coffee_machine_response = products_controller_pb2.CoffeeMachineResponse(**coffee_machine_args)

# Create LedMode Object
request = products_controller_pb2.ColorModeRequest(name="ihihih", color="#1234df")
response = products_controller_pb2.ColorModeResponse(name="ihihih", color="#1234df")
led_mode_request = products_controller_pb2.LedModeRequest()
led_mode_request.ColorMode.CopyFrom(request)
led_mode_response = products_controller_pb2.LedModeResponse()
led_mode_response.ColorMode.CopyFrom(response)
# Create LedPanel Object
led_panel_args = {
    "id": 3,
    "name": "oujih",
    "status": 3,
    "brightness": 0.05,
    "mode": led_mode_request,
    "categories": [category_request],
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

project_date = datetime.now()
request = products_controller_pb2.ProjectRequest(
    id=1,
    name="project smth",
    owner=1,
    pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
    products=[base_product_1_request, base_product_2_request],
)

response = products_controller_pb2.ProjectResponse(
    id=1,
    name="project smth",
    owner=1,
    pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
    products=[base_product_1_response, base_product_2_response],
)


class ProjectServicer(products_controller_pb2_grpc.ProjectControllerServicer):
    async def Create(self, *args, **kwargs):
        print(args, kwargs)
        return response

    async def List(self, *args, **kwargs):
        print(args, kwargs)
        return products_controller_pb2.ProjectListResponse(results=[response], count=1)


async def serve() -> None:
    server = grpc.aio.server()
    products_controller_pb2_grpc.add_ProjectControllerServicer_to_server(ProjectServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


logging.basicConfig(level=logging.INFO)
asyncio.get_event_loop().run_until_complete(serve())
