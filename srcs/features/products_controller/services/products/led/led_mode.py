from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

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
from features.products_controller.services.iot_mixin import IotMixin


class LedModeService(IotMixin):
    queryset = LedMode.objects.all()
    serializer_class = LedModeSerializer

    # Filter / Search / Order settings
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]


class ImageModeService(IotMixin):
    queryset = ImageMode.objects.all()
    serializer_class = ImageModeSerializer


class VideoModeService(IotMixin):
    queryset = VideoMode.objects.all()
    serializer_class = VideoModeSerializer


class ColorModeService(IotMixin):
    queryset = ColorMode.objects.all()
    serializer_class = ColorModeSerializer


class PatternModeService(IotMixin):
    queryset = PatternMode.objects.all()
    serializer_class = PatternModeSerializer
