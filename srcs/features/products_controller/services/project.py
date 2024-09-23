from features.products_controller.models.project import Project
from features.products_controller.serializers.project import ProjectSerializer
from features.products_controller.services.iot_mixin import IotMixin


class ProjectService(IotMixin):
    # https://django-socio-grpc.readthedocs.io/en/stable/features/authentication-permissions.html
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
