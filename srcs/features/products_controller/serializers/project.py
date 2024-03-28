from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    ProjectListResponse,
    ProjectResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from features.products_controller.serializers.products.base_product import (
    BaseProductSerializer,
    ProjectPolymorphicSerializer,
)


class ProjectSerializer(proto_serializers.ModelProtoSerializer):
    products = ProjectPolymorphicSerializer(many=True)

    # https://www.geeksforgeeks.org/prefetch_related-and-select_related-functions-in-django/
    class Meta:
        model = Project
        fields = "__all__"

        proto_class = ProjectResponse
        proto_class_list = ProjectListResponse

    def is_valid(self, raise_exception=True):
        print(f"ProjectSerializer.is_valid {self.initial_data=}")
        new_products = []
        for p in self.initial_data.get("products"):
            if "coffee_machine" in p.keys():
                p["coffee_machine"]["resourcetype"] = "CoffeeMachine"
            elif "led_panel" in p.keys():
                p["led_panel"]["resourcetype"] = "LedPanel"
            new_products.append(p)
        self.initial_data["products"] = new_products
        print(self.initial_data)
        # see, need to add a resourcetype to allow serializing
        # https://github.com/denisorehovsky/django-rest-polymorphic/blob/master/tests/test_serializers.py
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        print(f"ProjectSerializer.create {validated_data=}")
        new_products = []
        products_data = validated_data.pop("products")
        for c in products_data:
            category = BaseProduct.objects.filter(id=c.get("id")).first()
            if category is None:
                serializer = BaseProductSerializer(data=c)
                serializer.is_valid(raise_exception=True)
                category = serializer.save()
            new_products.append(category)

        instance = BaseProduct.objects.create(**validated_data)
        instance.products.set(new_products)
        return instance
