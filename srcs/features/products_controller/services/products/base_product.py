from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.serializers.products.base_product import (
    BaseProductSerializer,
)
from features.products_controller.services.iot_mixin import IotMixin


class BaseProductService(IotMixin):
    queryset = BaseProduct.objects.all()
    serializer_class = BaseProductSerializer

    # Filter / Search / Order settings
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
    filterset_fields = ["name", "categories__name"]
    search_fields = ["name", "categories__name"]
    ordering_fields = ["name", "categories__name"]
