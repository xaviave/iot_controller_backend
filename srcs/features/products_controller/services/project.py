from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework.pagination import PageNumberPagination

from features.products_controller.models.project import Project
from features.products_controller.serializers.project import ProjectSerializer
from features.products_controller.services.iot_mixin import IotMixin


class ProjectService(IotMixin):
    # https://django-socio-grpc.readthedocs.io/en/stable/features/authentication-permissions.html
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination

    # Filter / Search / Order settings
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
    filterset_fields = ["owner__username", "name", "pub_date"]
    search_fields = ["owner__username", "name", "pub_date"]
    ordering_fields = ["owner__username", "name", "pub_date"]
