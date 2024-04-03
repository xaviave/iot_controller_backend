import os

import cv2
from django.core.files.base import ContentFile
from django.db import models
from features.products_controller.models.products.led.led_mode import LedMode


class ImageMode(LedMode):
    image = models.ImageField(upload_to="images/")
    image_low_pixel = models.ImageField(upload_to="low_pixel_images/", null=True, blank=True)

    def generate_image_low_pixel(self, led_matrix_size: tuple) -> ContentFile:
        img_path = os.path.join(self.image.storage.location, self.image.path)
        pixel_img = cv2.resize(cv2.imread(img_path), dsize=led_matrix_size, interpolation=cv2.INTER_AREA)
        ret, buf = cv2.imencode(".jpg", pixel_img)
        return ContentFile(buf.tobytes())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.image_low_pixel:
            self.image_low_pixel.save(
                f"{os.path.splitext(os.path.basename(self.image.name))[0]}.png",
                self.generate_image_low_pixel(led_matrix_size=(8, 8)),
                save=False,
            )
            super().save(*args, **kwargs)

    def get_grpc_cmd(self) -> dict:
        return {
            "fn_name": "SetImage",
            "class_name": "Image",
            "w": self.image_low_pixel.width_field,
            "h": self.image_low_pixel.height_field,
            "bytes": ["ff"],
        }
