from django_celery_beat.models import IntervalSchedule
from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    IntervalScheduleListResponse,
    IntervalScheduleResponse,
)


class IntervalScheduleSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = IntervalSchedule
        fields = "__all__"

        proto_class = IntervalScheduleResponse
        proto_class_list = IntervalScheduleListResponse
