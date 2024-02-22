import os

import cv2
from colorfield.fields import ColorField
from django import forms
from django.core.files.base import ContentFile
from django.db import models
from features.products_controller.models.products.led.palette import Palette
from PIL import ImageColor
from polymorphic.models import PolymorphicModel


class LedMode(PolymorphicModel):
    name = models.CharField(max_length=200, unique=True)
    # add a field for temporary mode that will be cleaned by celery

    @property
    def has_mode(self):
        return True

    @classmethod
    def mode_names(cls):
        return [m.__name__ for m in cls.__subclasses__()]

    @staticmethod
    def get_form(*args, **kwargs):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def get_mode_choices(self):
        return self.objects.all()

    def get_grpc_cmd(self) -> dict:
        raise NotImplementedError


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

    @staticmethod
    def get_form():
        return CreateImageModeForm

    def get_grpc_cmd(self) -> dict:
        return {
            "fn_name": "SetImage",
            "class_name": "Image",
            "w": self.image_low_pixel.width_field,
            "h": self.image_low_pixel.height_field,
            "bytes": ["ff"],
        }


class CreateImageModeForm(forms.ModelForm):
    class Meta:
        model = ImageMode
        fields = ["name", "image"]


class VideoMode(LedMode):
    video = models.FileField(upload_to="videos/")
    video_low_pixel = models.ImageField(upload_to="video_low_pixels/", null=True, blank=True)

    def generate_video_low_pixel(self, video_matrix_size: tuple) -> ContentFile:
        video_path = os.path.join(self.video.storage.location, self.video.path)
        tmp_path = os.path.join(self.video.storage.location, "tmp")
        output_path = f"""{os.path.join(tmp_path, os.path.splitext(os.path.basename(self.video.name))[0])}.mp4"""

        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        cap = cv2.VideoCapture(video_path)
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), int(cap.get(5)), video_matrix_size)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            resized_frame = cv2.resize(frame, video_matrix_size)
            out.write(resized_frame)

        cap.release()
        out.release()

        with open(output_path, "rb") as video_file:
            content = video_file.read()

        os.remove(output_path)
        return ContentFile(content)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.video_low_pixel:
            self.video_low_pixel.save(
                f"{os.path.splitext(os.path.basename(self.video.name))[0]}.mp4",
                self.generate_video_low_pixel(video_matrix_size=(8, 8)),
                save=False,
            )
            super().save(*args, **kwargs)

    @staticmethod
    def get_form(*args, **kwargs):
        return CreateVideoModeForm

    def get_grpc_cmd(self) -> dict:
        return {
            "fn_name": "SetImage",
            "class_name": "Image",
            "w": self.image_low_pixel.width_field,
            "h": self.image_low_pixel.height_field,
            "bytes": ["ff"],
        }


class CreateVideoModeForm(forms.ModelForm):
    class Meta:
        model = VideoMode
        fields = ["name", "video"]


class ColorMode(LedMode):
    color = ColorField()

    @staticmethod
    def get_form(*args, **kwargs):
        return CreateColorModeForm

    def get_grpc_cmd(self) -> dict:
        r, g, b = ImageColor.getcolor(self.color, "RGB")
        return {"fn_name": "SetColor", "class_name": "Color", "r": r, "g": g, "b": b}


class CreateColorModeForm(forms.ModelForm):
    color = forms.CharField(widget=forms.TextInput(attrs={"type": "color"}))

    class Meta:
        model = ColorMode
        fields = ["name"]


class PatternMode(LedMode):
    fps = models.DecimalField(max_digits=5, decimal_places=2)
    blink = models.DecimalField(max_digits=4, decimal_places=2)
    palette = models.CharField(choices=[(choice.name, choice.name) for choice in Palette])

    @staticmethod
    def get_form(*args, **kwargs):
        return CreatePatternModeForm

    def get_grpc_cmd(self) -> dict:
        print(Palette[self.palette].grpc_data())
        return {
            "fn_name": "SetPattern",
            "class_name": "Pattern",
            "fps": self.fps,
            "blink": self.blink,
            "palette": Palette[self.palette].grpc_data(),
        }


class CreatePatternModeForm(forms.ModelForm):
    class Meta:
        model = PatternMode
        fields = ["name", "fps", "blink", "palette"]
