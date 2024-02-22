# serializers.py
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.products.coffee_machine import CoffeeMachine
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.serializers.products.coffee_machine import (
    CoffeeMachineSerializer,
)
from features.products_controller.serializers.products.led.led_panel import (
    LedPanelSerializer,
)
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProduct
        fields = "__all__"


class BaseProductPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        BaseProduct: BaseProductSerializer,
        CoffeeMachine: CoffeeMachineSerializer,
        LedPanel: LedPanelSerializer,
    }
