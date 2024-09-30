from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework.pagination import PageNumberPagination

from features.products_controller.models.category import Category
from features.products_controller.serializers.category import CategorySerializer
from features.products_controller.services.iot_mixin import IotMixin


class CategoryService(IotMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    # Filter / Search / Order settings
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
    filterset_fields = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    ordering_fields = [
        "name",
    ]
