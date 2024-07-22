from django_celery_beat.models import ClockedSchedule
from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    ClockedScheduleListResponse,
    ClockedScheduleResponse,
)


class ClockedScheduleSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = ClockedSchedule
        fields = "__all__"

        proto_class = ClockedScheduleResponse
        proto_class_list = ClockedScheduleListResponse
