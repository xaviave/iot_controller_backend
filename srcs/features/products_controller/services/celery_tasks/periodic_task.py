from django_celery_beat.models import PeriodicTask
from django_socio_grpc import generics

from features.products_controller.serializers.celery_tasks.periodic_task import PeriodicTaskSerializer


class PeriodicTaskService(generics.AsyncModelService):
    lookup_field = "name"
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
