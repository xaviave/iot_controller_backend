from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    CategoryListResponse,
    CategoryResponse,
)
from features.products_controller.models.category import Category
from rest_framework import serializers


class CategorySerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField(validators=[])

    class Meta:
        model = Category
        fields = "__all__"

        proto_class = CategoryResponse
        proto_class_list = CategoryListResponse
