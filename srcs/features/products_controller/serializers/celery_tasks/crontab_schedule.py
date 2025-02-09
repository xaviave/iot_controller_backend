from zoneinfo import ZoneInfo

from django_celery_beat.models import CrontabSchedule
from django_socio_grpc import proto_serializers

from base_app import settings
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

    def to_representation(self, instance):
        d = super().to_representation(instance)
        # IANA time zone database as String

        d["timezone"] = instance.timezone.key
        return d

    def to_internal_value(self, data):
        # IANA time zone database as String
        # Flutter can;t provide a robust timezone depending on the platform rn
        data["timezone"] = ZoneInfo(key=settings.TIME_ZONE)
        return super().to_internal_value(data)
