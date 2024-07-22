from django_celery_beat.models import SolarSchedule
from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import SolarScheduleListResponse, SolarScheduleResponse


class SolarScheduleSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = SolarSchedule
        fields = "__all__"
        #
        proto_class = SolarScheduleResponse
        proto_class_list = SolarScheduleListResponse
