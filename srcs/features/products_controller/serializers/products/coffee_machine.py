from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    CoffeeMachineListResponse,
    CoffeeMachineResponse,
)
from features.products_controller.models.category import Category
from features.products_controller.models.products.coffee_machine import CoffeeMachine
from features.products_controller.serializers.category import CategorySerializer


class CoffeeMachineSerializer(proto_serializers.ModelProtoSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = CoffeeMachine
        fields = "__all__"

        proto_class = CoffeeMachineResponse
        proto_class_list = CoffeeMachineListResponse

    def create(self, validated_data):
        new_categories = [
            Category.objects.get_or_create(name=c.get("name"))[0] for c in validated_data.pop("categories", [])
        ]

        instance = CoffeeMachine.objects.create(**validated_data)
        instance.categories.set(new_categories)
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.status = validated_data.get("status", instance.status)
        instance.heat = validated_data.get("heat", instance.heat)
        instance.water_level = validated_data.get("water_level", instance.water_level)
        instance.used_water_level = validated_data.get("used_water_level", instance.used_water_level)
        instance.coffee_level = validated_data.get("coffee_level", instance.coffee_level)
        instance.filter_position = validated_data.get("filter_position", instance.filter_position)
        instance.mode_value = validated_data.get("mode_value", instance.mode_value)
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
