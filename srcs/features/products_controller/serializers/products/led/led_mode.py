from django_socio_grpc import proto_serializers
from rest_framework import serializers
from rest_framework.fields import empty
from rest_polymorphic.serializers import PolymorphicSerializer

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
from features.products_controller.models.products.led.color_mode import ColorMode
from features.products_controller.models.products.led.image_mode import ImageMode
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.models.products.led.pattern_mode import PatternMode
from features.products_controller.models.products.led.video_mode import VideoMode


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

    def run_validation(self, data=empty):
        # MR https://github.com/denisorehovsky/django-rest-polymorphic/pull/31/files
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        resource_type = self._get_resource_type_from_mapping(data)
        serializer = self._get_serializer_from_resource_type(resource_type)
        validated_data = serializer.run_validation(data)
        validated_data[self.resource_type_field_name] = resource_type
        return validated_data
