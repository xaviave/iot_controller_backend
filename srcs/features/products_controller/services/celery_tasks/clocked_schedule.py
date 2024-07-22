from django_celery_beat.models import ClockedSchedule
from django_socio_grpc import generics
from features.products_controller.serializers.celery_tasks.clocked_schedule import ClockedScheduleSerializer


class ClockedScheduleService(generics.AsyncModelService):
    queryset = ClockedSchedule.objects.all()
    serializer_class = ClockedScheduleSerializer
