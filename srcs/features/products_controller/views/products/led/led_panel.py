from django_socio_grpc import generics
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.serializers.products.led.led_panel import (
    LedPanelSerializer,
)


class LedPanelService(generics.AsyncModelService):
    queryset = LedPanel.objects.all()
    serializer_class = LedPanelSerializer
