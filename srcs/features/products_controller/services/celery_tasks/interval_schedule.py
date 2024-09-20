from django_celery_beat.models import IntervalSchedule
from django_socio_grpc import generics

from features.products_controller.serializers.celery_tasks.interval_schedule import IntervalScheduleSerializer


class IntervalScheduleService(generics.AsyncModelService):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
