from django_celery_beat.models import PeriodicTask
from django_filters import rest_framework as rest_filters
from django_socio_grpc import generics
from rest_framework import filters

from features.products_controller.serializers.celery_tasks.periodic_task import PeriodicTaskSerializer


class PeriodicTaskService(generics.AsyncModelService):
    lookup_field = "name"
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer

    # Filter / Search / Order settings
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ["name", "task"]
    ordering_fields = ["name", "start_time", "enabled"]
    search_fields = ["name", "task"]
