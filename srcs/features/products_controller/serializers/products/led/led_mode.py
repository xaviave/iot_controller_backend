from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    ColorModeListResponse,
    ColorModeResponse,
    ImageModeListResponse,
    ImageModeResponse,
    LedModeResponse,
    PatternModeListResponse,
    PatternModeResponse,
    VideoModeListResponse,
    VideoModeResponse,
)
from features.products_controller.models.products.led.led_mode import (
    ColorMode,
    ImageMode,
    LedMode,
    PatternMode,
    VideoMode,
)
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class LedModeSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = LedMode
        fields = "__all__"

        proto_class = LedModeResponse


class ImageModeSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = ImageMode
        fields = "__all__"

        proto_class = ImageModeResponse
        proto_class_list = ImageModeListResponse


class VideoModeSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = VideoMode
        fields = "__all__"

        proto_class = VideoModeResponse
        proto_class_list = VideoModeListResponse


class ColorModeSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = ColorMode
        fields = "__all__"

        proto_class = ColorModeResponse
        proto_class_list = ColorModeListResponse


class PatternModeSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = PatternMode
        fields = "__all__"

        proto_class = PatternModeResponse
        proto_class_list = PatternModeListResponse


class LedModePolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        LedMode: LedModeSerializer,
        ImageMode: ImageModeSerializer,
        VideoMode: VideoModeSerializer,
        ColorMode: ColorModeSerializer,
        PatternMode: PatternModeSerializer,
    }
