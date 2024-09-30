from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, PeriodicTask, SolarSchedule
from django_socio_grpc import proto_serializers

from features.products_controller.grpc.products_controller_pb2 import PeriodicTaskListResponse, PeriodicTaskResponse
from features.products_controller.serializers.celery_tasks.clocked_schedule import ClockedScheduleSerializer
from features.products_controller.serializers.celery_tasks.crontab_schedule import CrontabScheduleSerializer
from features.products_controller.serializers.celery_tasks.interval_schedule import IntervalScheduleSerializer
from features.products_controller.serializers.celery_tasks.solar_schedule import SolarScheduleSerializer


class PeriodicTaskSerializer(proto_serializers.ModelProtoSerializer):
    clocked = ClockedScheduleSerializer(required=False)
    crontab = CrontabScheduleSerializer(required=False)
    interval = IntervalScheduleSerializer(required=False)
    solar = SolarScheduleSerializer(required=False)

    class Meta:
        model = PeriodicTask
        fields = ["name", "task", "enabled", "kwargs", "clocked", "crontab", "interval", "solar"]

        proto_class = PeriodicTaskResponse
        proto_class_list = PeriodicTaskListResponse

    """

    def create(self, validated_data):
        validated_data["task"] = f"srcs.features.products_controller.tasks.{validated_data['task']}"
        schedule_types = {
            "clocked": (ClockedSchedule, ClockedScheduleSerializer, ["clocked_time"]),
            "crontab": (CrontabSchedule, CrontabScheduleSerializer,
                        ["minute", "hour", "day_of_month", "month_of_year", "day_of_week", "timezone"]),
            "interval": (IntervalSchedule, IntervalScheduleSerializer, ["every", "period"]),
            "solar": (SolarSchedule, SolarScheduleSerializer, ["event", "latitude", "longitude"])
        }

        for schedule_type, (model, serializer_class, fields) in schedule_types.items():
            if schedule_type in validated_data:
                validated_data[schedule_type] = self.get_or_create_schedule(
                    validated_data.pop(schedule_type),
                    model,
                    serializer_class,
                    fields
                )

        instance = PeriodicTask.objects.create(**validated_data)
        return instance

    def get_or_create_schedule(self, schedule_data, model, serializer_class, unique_fields):
        try:
            filter_kwargs = {field: schedule_data.get(field) for field in unique_fields}
            return model.objects.get(**filter_kwargs)
        except model.DoesNotExist:
            serializer = serializer_class(data=schedule_data)
            serializer.is_valid(raise_exception=True)
            return serializer.save()
    """

    def create(self, validated_data):
        validated_data["task"] = f"features.products_controller.tasks.{validated_data['task']}"

        if validated_data.get("clocked") is not None:
            try:
                clocked = ClockedSchedule.objects.get(clocked_time=validated_data.get("clocked").get("clocked_time"))
            except ClockedSchedule.DoesNotExist:
                serializer = ClockedScheduleSerializer(data=validated_data.get("clocked"))
                serializer.is_valid(raise_exception=True)
                clocked = serializer.save()
            validated_data["clocked"] = clocked
            validated_data["one_off"] = True
        elif validated_data.get("crontab") is not None:
            try:
                crontab = CrontabSchedule.objects.get(
                    minute=validated_data.get("crontab").get("minute"),
                    hour=validated_data.get("crontab").get("hour"),
                    day_of_month=validated_data.get("crontab").get("day_of_month"),
                    month_of_year=validated_data.get("crontab").get("month_of_year"),
                    day_of_week=validated_data.get("crontab").get("day_of_week"),
                    timezone=validated_data.get("crontab").get("timezone"),
                )
            except CrontabSchedule.DoesNotExist:
                serializer = CrontabScheduleSerializer(data=validated_data.get("crontab"))
                serializer.is_valid(raise_exception=True)
                crontab = serializer.save()
            validated_data["crontab"] = crontab
        elif validated_data.get("interval") is not None:
            try:
                interval = IntervalSchedule.objects.get(
                    every=validated_data.get("interval").get("every"),
                    period=validated_data.get("interval").get("period"),
                )
            except IntervalSchedule.DoesNotExist:
                serializer = IntervalScheduleSerializer(data=validated_data.get("interval"))
                serializer.is_valid(raise_exception=True)
                interval = serializer.save()
            validated_data["interval"] = interval
        elif validated_data.get("solar") is not None:
            try:
                solar = SolarSchedule.objects.get(
                    event=validated_data.get("solar").get("event"),
                    latitude=validated_data.get("solar").get("latitude"),
                    longitude=validated_data.get("solar").get("longitude"),
                )
            except SolarSchedule.DoesNotExist:
                serializer = SolarScheduleSerializer(data=validated_data.get("solar"))
                serializer.is_valid(raise_exception=True)
                solar = serializer.save()
            validated_data["solar"] = solar

        return PeriodicTask.objects.create(**validated_data)
