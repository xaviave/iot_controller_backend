from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    ProjectListResponse,
    ProjectResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.serializers.products.base_product import BaseProductSerializer
from features.products_controller.models.project import Project
from rest_framework.serializers import PrimaryKeyRelatedField, UUIDField

class ProjectSerializer(proto_serializers.ModelProtoSerializer):
    products = BaseProductSerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"

        proto_class = ProjectResponse
        proto_class_list = ProjectListResponse
