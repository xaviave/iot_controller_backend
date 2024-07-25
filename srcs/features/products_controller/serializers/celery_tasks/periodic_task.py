from django_celery_beat.models import PeriodicTask
from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import PeriodicTaskListResponse, PeriodicTaskResponse
from features.products_controller.serializers.celery_tasks.clocked_schedule import ClockedScheduleSerializer
from features.products_controller.serializers.celery_tasks.crontab_schedule import CrontabScheduleSerializer
from features.products_controller.serializers.celery_tasks.interval_schedule import IntervalScheduleSerializer
from features.products_controller.serializers.celery_tasks.solar_schedule import SolarScheduleSerializer


class PeriodicTaskSerializer(proto_serializers.ModelProtoSerializer):
    clocked = ClockedScheduleSerializer()
    crontab = CrontabScheduleSerializer()
    interval = IntervalScheduleSerializer()
    solar = SolarScheduleSerializer()

    class Meta:
        model = PeriodicTask
        fields = ["name", "task", "kwargs", "clocked", "crontab", "interval", "solar"]

        proto_class = PeriodicTaskResponse
        proto_class_list = PeriodicTaskListResponse

    def create(self, validated_data):
        # classes = {"Project": Project, "BaseProduct": BaseProduct}
        # class_type = classes[kwargs.pop("class_type")]
        # obj = class_type.objects.get(id=kwargs.pop("class_id"))

        validated_data.task = f"srcs.features.products_controller.tasks.{validated_data['task']}"

        instance = PeriodicTask.objects.create(**validated_data)
        return instance
