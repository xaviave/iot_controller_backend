from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    LedModeListResponse,
    LedModeResponse,
)
from features.products_controller.models.products.led.led_mode import (
    ColorMode,
    ImageMode,
    LedMode,
    PatternMode,
    VideoMode,
)
from rest_framework import serializers


class LedModeSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = LedMode
        fields = "__all__"

        proto_class = LedModeResponse
        proto_class_list = LedModeListResponse


class ImageModeSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = ImageMode
        fields = "__all__"


class VideoModeSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = VideoMode
        fields = "__all__"


class ColorModeSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = ColorMode
        fields = "__all__"


class PatternModeSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = PatternMode
        fields = "__all__"
