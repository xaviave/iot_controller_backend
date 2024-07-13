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
        """
        Update django server DB
        Send request to the client as a new Update Request from the updated object
        """
        message = await super().Update(request, context)
        # need to add a filter of the vars that have to update the task
        led = await self.aget_object()
        led_request = await sync_to_async(led.get_grpc_request)()
        stub = await sync_to_async(led.get_stub)()
        self.grpc_request(stub, led_request)
        return message

    async def PartialUpdate(self, request, context):
        message = await super().PartialUpdate(request, context)
        # need to add a filter of the vars that have to update the task
        led = await self.aget_object()
        led_request = await sync_to_async(led.get_grpc_request)()
        stub = await sync_to_async(led.get_stub)()
        self.grpc_request(stub, led_request)
        return message
