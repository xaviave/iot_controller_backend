from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    BaseProductResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.products.coffee_machine import CoffeeMachine
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.serializers.category import CategorySerializer
from features.products_controller.serializers.products.coffee_machine import CoffeeMachineSerializer
from features.products_controller.serializers.products.led.led_panel import LedPanelSerializer
from rest_polymorphic.serializers import PolymorphicSerializer


class BaseProductSerializer(proto_serializers.ModelProtoSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = BaseProduct
        fields = "__all__"

        proto_class = BaseProductResponse
        # proto_class_list = BaseProductListResponse


    def is_valid(self, *, raise_exception=False):
        print(f"BaseProductSerializer.is_valid {self.initial_data=}")
        exit()
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        print(f"BaseProductSerializer.create {validated_data=}"); exit()


class ProjectPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        BaseProduct: BaseProductSerializer,
        LedPanel: LedPanelSerializer,
        CoffeeMachine: CoffeeMachineSerializer,
    }
