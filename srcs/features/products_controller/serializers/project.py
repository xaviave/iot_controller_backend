from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    ProjectListResponse,
    ProjectResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from rest_framework.serializers import PrimaryKeyRelatedField, UUIDField

# https://www.django-rest-framework.org/api-guide/relations/
class ProjectSerializer(proto_serializers.ModelProtoSerializer):
    products = PrimaryKeyRelatedField(
        queryset=BaseProduct.objects.all(),
        pk_field=UUIDField(format="hex_verbose"),
        many=True,
    )

    class Meta:
        model = Project
        fields = "__all__"

        proto_class = ProjectResponse
        proto_class_list = ProjectListResponse
