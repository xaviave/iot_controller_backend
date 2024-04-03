from colorfield.fields import ColorField
from features.products_controller.models.products.led.led_mode import LedMode
from PIL import ImageColor


class ColorMode(LedMode):
    color = ColorField()

    def get_grpc_cmd(self) -> dict:
        r, g, b = ImageColor.getcolor(self.color, "RGB")
        return {"fn_name": "SetColor", "class_name": "Color", "r": r, "g": g, "b": b}
