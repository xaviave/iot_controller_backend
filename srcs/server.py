import asyncio
import logging
from concurrent import futures
from datetime import datetime

import grpc
from features.products_controller.grpc import (
    test_polymorphism_pb2,
    test_polymorphism_pb2_grpc,
)

# Create Category Object
category_request = test_polymorphism_pb2.CategoryRequest(id=1, name="cate")
category_response = test_polymorphism_pb2.CategoryResponse(id=1, name="cate")

# Create LedMode Object
led_mode_request = test_polymorphism_pb2.LedModeRequest(id=1, name="mode smth")
led_mode_response = test_polymorphism_pb2.LedModeResponse(id=1, name="mode smth")

# Create CoffeeMachine Object
coffee_machine_args = {
    "id":1,
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
coffee_machine_request = test_polymorphism_pb2.CoffeeMachineRequest(**coffee_machine_args)
coffee_machine_args["categories"] = [category_response]
coffee_machine_response = test_polymorphism_pb2.CoffeeMachineResponse(**coffee_machine_args)

# Create LedMode Object
led_mode_request = test_polymorphism_pb2.LedModeRequest(id=3, name="mode smth")
led_mode_response = test_polymorphism_pb2.LedModeResponse(id=3, name="mode smth")

# Create LedPanel Object
led_panel_args = {
    "id":3,
    "name": "oujih",
    "status": 3,
    "brightness": 0.05,
    "mode": led_mode_request,
    "categories": [category_request],
}

led_panel_request = test_polymorphism_pb2.LedPanelRequest(**led_panel_args)
led_panel_args["mode"] = led_mode_response
led_panel_args["categories"] = [category_response]
led_panel_response = test_polymorphism_pb2.LedPanelResponse(**led_panel_args)

base_product_1_request = test_polymorphism_pb2.BaseProductRequest()
base_product_1_request.coffee_machine.CopyFrom(coffee_machine_request)
base_product_1_response = test_polymorphism_pb2.BaseProductResponse()
base_product_1_response.coffee_machine.CopyFrom(coffee_machine_response)

base_product_2_request = test_polymorphism_pb2.BaseProductRequest()
base_product_2_request.led_panel.CopyFrom(led_panel_request)
base_product_2_response = test_polymorphism_pb2.BaseProductResponse()
base_product_2_response.led_panel.CopyFrom(led_panel_response)

project_date = datetime.now()
request = test_polymorphism_pb2.ProjectRequest(
    id=1,
    name="project smth",
    owner=1,
    pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
    products=[base_product_1_request, base_product_2_request],
)

response = test_polymorphism_pb2.ProjectResponse(
    id=1,
    name="project smth",
    owner=1,
    pub_date=project_date.strftime("%Y-%m-%dT%H:%M:%S"),
    products=[base_product_1_response, base_product_2_response],
)


class ProjectServicer(test_polymorphism_pb2_grpc.ProjectControllerServicer):
    async def Create(self, request):
        print(request)
        return response

    async def List(self, *args, **kwargs):
        print(args, kwargs)
        return test_polymorphism_pb2.ProjectListResponse(results=[response], count=1)


async def serve() -> None:
    server = grpc.aio.server()
    test_polymorphism_pb2_grpc.add_ProjectControllerServicer_to_server(ProjectServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()

logging.basicConfig(level=logging.INFO)
asyncio.get_event_loop().run_until_complete(serve())
