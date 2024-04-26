from features.products_controller.models.products.coffee_machine import CoffeeMachine
from features.products_controller.serializers.products.coffee_machine import (
    CoffeeMachineSerializer,
)
from features.products_controller.services.iot_mixin import IotMixin


class CoffeeMachineService(IotMixin):
    queryset = CoffeeMachine.objects.all()
    serializer_class = CoffeeMachineSerializer
