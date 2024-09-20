from django_socio_grpc import proto_serializers
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from features.products_controller.grpc.products_controller_pb2 import (
    BaseProductResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.products.coffee_machine import CoffeeMachine
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.serializers.category import CategorySerializer
from features.products_controller.serializers.products.coffee_machine import (
    CoffeeMachineSerializer,
)
from features.products_controller.serializers.products.led.led_panel import (
    LedPanelSerializer,
)


class BaseProductSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField(validators=[])
    categories = CategorySerializer(many=True)
    ip_address = serializers.CharField(validators=[])
    ip_port = serializers.IntegerField()

    class Meta:
        model = BaseProduct
        fields = "__all__"

        proto_class = BaseProductResponse
        # proto_class_list = BaseProductListResponse


class BaseProductPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        BaseProduct: BaseProductSerializer,
        LedPanel: LedPanelSerializer,
        CoffeeMachine: CoffeeMachineSerializer,
    }
