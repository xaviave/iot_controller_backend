from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    CoffeeMachineListResponse,
    CoffeeMachineResponse,
)
from features.products_controller.models.products.coffee_machine import CoffeeMachine


class CoffeeMachineSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = CoffeeMachine
        fields = "__all__"

        proto_class = CoffeeMachineResponse
        proto_class_list = CoffeeMachineListResponse
