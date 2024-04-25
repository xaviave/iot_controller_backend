from asgiref.sync import sync_to_async
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.serializers.products.led.led_panel import (
    LedPanelSerializer,
)
from features.products_controller.services.iot_mixin import IotMixin


class LedPanelService(IotMixin):
    queryset = LedPanel.objects.all()
    serializer_class = LedPanelSerializer

    async def Update(self, request, context):
        message = await super().Update(request, context)
        led = await self.aget_object()
        led_request = await sync_to_async(led.get_grpc_request)()
        await self.grpc_request(await sync_to_async(led.get_stub)(), led_request)
        return message
