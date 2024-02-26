from django_socio_grpc import proto_serializers
from features.products_controller.grpc.products_controller_pb2 import (
    LedPanelListResponse,
    LedPanelResponse,
)
from features.products_controller.models.products.led.led_panel import LedPanel


class LedPanelSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = LedPanel
        fields = "__all__"

        proto_class = LedPanelResponse
        proto_class_list = LedPanelListResponse
