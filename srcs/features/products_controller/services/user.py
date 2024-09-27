from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from features.products_controller.serializers.user import UserSerializer
from features.products_controller.services.iot_mixin import IotMixin


class UserService(IotMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Filter / Search / Order settings
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
    filterset_fields = ["username", "email"]
    search_fields = ["username", "first_name", "last_name"]
    ordering_fields = ["username", "first_name", "last_name"]
