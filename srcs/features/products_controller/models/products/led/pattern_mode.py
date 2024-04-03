from django.db import models
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.models.products.led.palette import Palette


class PatternMode(LedMode):
    fps = models.DecimalField(max_digits=5, decimal_places=2)
    blink = models.DecimalField(max_digits=4, decimal_places=2)
    palette = models.CharField(choices=[(choice.name, choice.name) for choice in Palette])

    def get_grpc_cmd(self) -> dict:
        print(Palette[self.palette].grpc_data())
        return {
            "fn_name": "SetPattern",
            "class_name": "Pattern",
            "fps": self.fps,
            "blink": self.blink,
            "palette": Palette[self.palette].grpc_data(),
        }
