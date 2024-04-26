from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.serializers.products.base_product import (
    BaseProductSerializer,
)
from features.products_controller.services.iot_mixin import IotMixin


class BaseProductService(IotMixin):
    queryset = BaseProduct.objects.all()
    serializer_class = BaseProductSerializer
