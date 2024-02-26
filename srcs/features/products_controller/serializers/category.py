from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    CategoryListResponse,
    CategoryResponse,
)
from features.products_controller.models.category import Category


class CategorySerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Category
        fields = "__all__"

        proto_class = CategoryResponse
        proto_class_list = CategoryListResponse
