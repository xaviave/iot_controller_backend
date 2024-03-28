from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    ProjectListResponse,
    ProjectResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from features.products_controller.serializers.products.base_product import (
    BaseProductSerializer,
)


class ProjectSerializer(proto_serializers.ModelProtoSerializer):
    products = BaseProductSerializer(many=True)

    # https://www.geeksforgeeks.org/prefetch_related-and-select_related-functions-in-django/
    class Meta:
        model = Project
        fields = "__all__"

        proto_class = ProjectResponse
        proto_class_list = ProjectListResponse

    def create(self, validated_data):
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
