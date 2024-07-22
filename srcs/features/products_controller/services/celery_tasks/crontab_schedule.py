from django_celery_beat.models import CrontabSchedule
from django_socio_grpc import generics
from features.products_controller.serializers.celery_tasks.crontab_schedule import CrontabScheduleSerializer


class CrontabScheduleService(generics.AsyncModelService):
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer
