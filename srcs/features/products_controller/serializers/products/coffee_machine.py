from features.products_controller.models.products.coffee_machine import CoffeeMachine
from rest_framework import serializers


class CoffeeMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeMachine
        fields = "__all__"
