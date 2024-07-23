from django_celery_beat.models import PeriodicTask
from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import PeriodicTaskListResponse, PeriodicTaskResponse
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from rest_framework import serializers


class PeriodicTaskSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField()
    task = serializers.CharField()

    class_type = serializers.CharField()
    class_id = serializers.CharField()

    class Meta:
        model = PeriodicTask
        fields = ["name", "task", "class_type", "class_id", "interval", "crontab", "solar", "clocked"]

        proto_class = PeriodicTaskResponse
        proto_class_list = PeriodicTaskListResponse

    def create(self, validated_data):
        classes = {"Project": Project, "BaseProduct": BaseProduct}
        class_type = classes[validated.pop("class_type")]
        obj = class_type.objects.get(id=validated_data.pop("class_id"))

        validated_data["args"] = {"obj": obj}
        validated_data.task = f"srcs.features.products_controller.tasks.{validated_data['task']}"

        instance = PeriodicTask.objects.create(**validated_data)
        return instance
