from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    BaseProductListResponse,
    BaseProductResponse,
)
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.serializers.category import CategorySerializer


class BaseProductSerializer(proto_serializers.ModelProtoSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = BaseProduct
        fields = "__all__"

        proto_class = BaseProductResponse
        proto_class_list = BaseProductListResponse
