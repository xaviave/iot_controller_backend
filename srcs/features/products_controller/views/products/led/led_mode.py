from django_socio_grpc import generics
from features.products_controller.models.products.led.color_mode import ColorMode
from features.products_controller.models.products.led.image_mode import ImageMode
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.models.products.led.pattern_mode import PatternMode
from features.products_controller.models.products.led.video_mode import VideoMode
from features.products_controller.serializers.products.led.led_mode import (
    ColorModeSerializer,
    ImageModeSerializer,
    LedModeSerializer,
    PatternModeSerializer,
    VideoModeSerializer,
)


class LedModeService(generics.AsyncModelService):
    queryset = LedMode.objects.all()
    serializer_class = LedModeSerializer


class ImageModeService(generics.AsyncModelService):
    queryset = ImageMode.objects.all()
    serializer_class = ImageModeSerializer


class VideoModeService(generics.AsyncModelService):
    queryset = VideoMode.objects.all()
    serializer_class = VideoModeSerializer


class ColorModeService(generics.AsyncModelService):
    queryset = ColorMode.objects.all()
    serializer_class = ColorModeSerializer


class PatternModeService(generics.AsyncModelService):
    queryset = PatternMode.objects.all()
    serializer_class = PatternModeSerializer
