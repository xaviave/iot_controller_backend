from django.contrib.auth.models import User
from django_socio_grpc import proto_serializers
from rest_framework import serializers

from features.products_controller.grpc.products_controller_pb2 import (
    UserListResponse,
    UserResponse,
)


class UserSerializer(proto_serializers.ModelProtoSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "groups"]

        proto_class = UserResponse
        proto_class_list = UserListResponse
