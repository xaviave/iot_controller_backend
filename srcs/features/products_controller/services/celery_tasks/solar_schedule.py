from django_celery_beat.models import SolarSchedule
from django_socio_grpc import generics

from features.products_controller.serializers.celery_tasks.solar_schedule import SolarScheduleSerializer


class SolarScheduleService(generics.AsyncModelService):
    queryset = SolarSchedule.objects.all()
    serializer_class = SolarScheduleSerializer
