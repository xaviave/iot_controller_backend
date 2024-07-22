from django_celery_beat.models import CrontabSchedule
from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    CrontabScheduleListResponse,
    CrontabScheduleResponse,
)


class CrontabScheduleSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = CrontabSchedule
        fields = "__all__"

        proto_class = CrontabScheduleResponse
        proto_class_list = CrontabScheduleListResponse
