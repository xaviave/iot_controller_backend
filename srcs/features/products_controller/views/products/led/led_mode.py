from django_socio_grpc import generics
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.serializers.products.led.led_mode import (
    LedModeSerializer,
)


class LedModeService(generics.AsyncModelService):
    queryset = LedMode.objects.all()
    serializer_class = LedModeSerializer
