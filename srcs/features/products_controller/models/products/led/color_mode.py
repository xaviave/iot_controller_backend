from colorfield.fields import ColorField
from features.products_controller.grpc import products_controller_pb2
from features.products_controller.models.products.led.led_mode import LedMode
from PIL import ImageColor


class ColorMode(LedMode):
    color = ColorField()

    def get_grpc_request(self) -> products_controller_pb2.LedModeRequest:
        grpc_request = products_controller_pb2.LedModeRequest()
        # print(self.color)
        grpc_request.ColorMode.CopyFrom(
            products_controller_pb2.ColorModeRequest(
                # FW doesn't need any metadata rn
                # id=self.id,
                # name=self.name,
                color=self.color,
            )
        )
        return grpc_request
