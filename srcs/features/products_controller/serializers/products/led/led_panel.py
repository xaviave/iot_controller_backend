from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    LedPanelListResponse,
    LedPanelResponse,
)
from features.products_controller.models.category import Category
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.serializers.category import CategorySerializer
from features.products_controller.serializers.products.led.led_mode import (
    LedModeSerializer,
)
from rest_framework import serializers


class LedPanelSerializer(proto_serializers.ModelProtoSerializer):
    mode = LedModeSerializer(many=False)
    name = serializers.CharField(validators=[])
    categories = CategorySerializer(many=True)

    class Meta:
        model = LedPanel
        fields = "__all__"

        proto_class = LedPanelResponse
        proto_class_list = LedPanelListResponse

    def create(self, validated_data):
        new_categories = [
            Category.objects.get_or_create(name=c.get("name"))[0] for c in validated_data.pop("categories", [])
        ]

        led_mode_data = validated_data.pop("mode")
        led_mode, _ = LedMode.objects.get_or_create(name=led_mode_data.get("name"))
        instance = LedPanel.objects.create(mode=led_mode, **validated_data)
        instance.categories.set(new_categories)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.brightness = validated_data.get("brightness", instance.brightness)
        instance.mode, _ = LedMode.objects.get_or_create(name=validated_data.get("mode", instance.mode))
        instance.save()

        new_categories = []
        categories = validated_data.pop("categories", instance.categories.all())
        for category in categories:
            if isinstance(category, Category):
                name = category.name
            else:
                name = category.get("name")
            new_categories.append(Category.objects.get_or_create(name=name)[0])
        instance.categories.set(new_categories)
        return instance
