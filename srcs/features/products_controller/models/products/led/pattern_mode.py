from colorfield.fields import ColorField
from django.contrib.postgres.fields.array import ArrayField
from django.db import models

from features.products_controller.grpc import products_controller_pb2
from features.products_controller.models.products.led.led_mode import LedMode


class PatternMode(LedMode):
    fps = models.DecimalField(max_digits=5, decimal_places=2)
    blink = models.DecimalField(max_digits=4, decimal_places=2)
    palette = ArrayField(ColorField(default="#FFFF"))

    def get_grpc_request(self) -> products_controller_pb2.LedModeRequest:
        grpc_request = products_controller_pb2.LedModeRequest()
        grpc_request.PatternMode.CopyFrom(
            products_controller_pb2.PatternModeRequest(
                # FW doesn't need any metadata rn
                # id=self.id,
                # name=self.name,
                fps=self.fps,
                blink=self.blink,
                palette=[c for c in self.palette],
            )
        )
        return grpc_request
