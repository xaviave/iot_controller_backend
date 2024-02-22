from features.products_controller.models.products.led.led_mode import (
    ColorMode,
    ImageMode,
    LedMode,
    PatternMode,
    VideoMode,
)
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class LedModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedMode
        fields = "__all__"


class ImageModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMode
        fields = "__all__"


class VideoModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoMode
        fields = "__all__"


class ColorModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorMode
        fields = "__all__"


class PatternModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatternMode
        fields = "__all__"


class LedModePolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        LedMode: LedModeSerializer,
        ImageMode: ImageModeSerializer,
        VideoMode: VideoModeSerializer,
        ColorMode: ColorModeSerializer,
        PatternMode: PatternModeSerializer,
    }
