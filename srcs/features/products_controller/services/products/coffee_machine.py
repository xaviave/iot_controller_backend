from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework.pagination import PageNumberPagination

from features.products_controller.models.products.coffee_machine import CoffeeMachine
from features.products_controller.serializers.products.coffee_machine import CoffeeMachineSerializer
from features.products_controller.services.iot_mixin import IotMixin


class CoffeeMachineService(IotMixin):
    queryset = CoffeeMachine.objects.all()
    serializer_class = CoffeeMachineSerializer
    pagination_class = PageNumberPagination

    # Filter / Search / Order settings
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
    filterset_fields = ["name", "categories__name"]
    search_fields = ["name", "categories__name"]
    ordering_fields = ["name", "categories__name"]
