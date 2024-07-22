from django_celery_beat.models import PeriodicTask
from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import PeriodicTaskListResponse, PeriodicTaskResponse
from rest_framework import serializers


class PeriodicTaskSerializer(proto_serializers.ModelProtoSerializer):
    name = serializers.CharField()
    task = serializers.CharField()

    class Meta:
        model = PeriodicTask
        fields = ["name", "task", "interval", "crontab", "solar", "clocked"]
        #
        proto_class = PeriodicTaskResponse
        proto_class_list = PeriodicTaskListResponse
