from django_socio_grpc import generics
from features.products_controller.models.products.coffee_machine import CoffeeMachine
from features.products_controller.serializers.products.coffee_machine import (
    CoffeeMachineSerializer,
)


class CoffeeMachineService(generics.AsyncModelService):
    queryset = CoffeeMachine.objects.all()
    serializer_class = CoffeeMachineSerializer
