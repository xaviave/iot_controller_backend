from functools import cached_property

from django.db import models
from features.products_controller.grpc import products_controller_pb2, products_controller_pb2_grpc
from features.products_controller.grpc import products_controller_pb2 as proto_lib
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.products.led.led_mode import LedMode
from features.products_controller.models.status import Status


class LedPanel(BaseProduct):
    status = models.IntegerField(choices=Status.choices())
    brightness = models.DecimalField(default=0.5, max_digits=3, decimal_places=2)
    mode = models.ForeignKey("LedMode", on_delete=models.SET_NULL, null=True)

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
        return products_controller_pb2_grpc.LedPanelControllerStub

    def get_grpc_request(self) -> products_controller_pb2.LedPanelRequest:
        print(self.mode)
        print(self.mode.get_grpc_request())
        return products_controller_pb2.LedPanelRequest(
            status=self.status,
            brightness=self.brightness,
            mode=self.mode.get_grpc_request(),
            categories=[],
            # FW doesn't need any metadata RN
            # id=self.id,
            # name=self.name,
            # categories=[c.get_grpc_request() for c in self.categories],
        )

    def __str__(self):
        return self.name

    def get_status(self):
        return Status(self.status).name.title()

    def get_mode(self) -> str:
        return f"{self.grpc_mode_value} {self.mode.name}"

    def get(self, *args, **kwargs): ...
