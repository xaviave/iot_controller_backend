from django_socio_grpc import proto_serializers

from features.products_controller.grpc.products_controller_pb2 import (
    ProjectListResponse,
    ProjectResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from features.products_controller.serializers.products.base_product import (
    BaseProductPolymorphicSerializer,
)


class ProjectSerializer(proto_serializers.ModelProtoSerializer):
    products = BaseProductPolymorphicSerializer(many=True)

    # https://www.geeksforgeeks.org/prefetch_related-and-select_related-functions-in-django/
    class Meta:
        model = Project
        fields = "__all__"

        proto_class = ProjectResponse
        proto_class_list = ProjectListResponse

    def to_internal_value(self, data):
        print(f"ProjectSerializer.to_internal_value")
        # data["owner"] = User.objects.get(id=data.get("owner"))
        new_products = []
        for p in data.get("products"):
            if "coffee_machine" in p.keys():
                p = {"resourcetype": "CoffeeMachine", **p["coffee_machine"]}
            elif "led_panel" in p.keys():
                p = {"resourcetype": "LedPanel", **p["led_panel"]}
            new_products.append(p)
        data["products"] = new_products
        # return data
        return super().to_internal_value(data)

    def create(self, validated_data):
        new_products = []
        products_data = validated_data.pop("products")
        for c in products_data:
            product = BaseProduct.objects.filter(id=c.get("id")).first()
            if product is None:
                serializer = BaseProductPolymorphicSerializer(data=c)
                serializer.is_valid(raise_exception=True)
                product = serializer.save()
            new_products.append(product)

        instance = Project.objects.create(**validated_data)
        instance.products.set(new_products)
        return instance


