from functools import cached_property

from django.db import models
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.models.status import Status
from grpc_iot.protos import led_communication_pb2 as proto_lib
from grpc_iot.protos import led_communication_pb2_grpc


class LedPanel(BaseProduct):
    status = models.IntegerField(choices=Status.choices())
    brightness = models.DecimalField(default=0.5, max_digits=3, decimal_places=2)
    mode = models.OneToOneField(LedMode, on_delete=models.CASCADE)

    @cached_property
    def html(self):
        return "products_controller/products/led_panel.html"

    @cached_property
    def get_proto_lib(self):
        return proto_lib

    @cached_property
    def grpc_mode_value(self):
        return type(self.mode).__name__

    @cached_property
    def mode_list(self):
        return LedMode.__subclasses__()

    @staticmethod
    def get_stub(channel):
        return led_communication_pb2_grpc.LedCommunicationStub(channel)

    def __str__(self):
        return self.name

    def get_status(self):
        return Status(self.status).name.title()

    def get_mode(self) -> str:
        return f"{self.grpc_mode_value} {self.mode.name}"

    def get(self, *args, **kwargs):
        ...
