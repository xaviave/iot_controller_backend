from enum import IntEnum

from django.db import models

from features.products_controller.grpc import products_controller_pb2_grpc
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.status import Status


class ContainerStatus(IntEnum):
    EMPTY = 0
    WARNING = 1
    FULL = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class CoffeeMachine(BaseProduct):
    status = models.IntegerField(choices=Status.choices())
    heat = models.FloatField(default=0.0)
    water_level = models.IntegerField(choices=ContainerStatus.choices(), default=ContainerStatus.EMPTY)
    used_water_level = models.IntegerField(choices=ContainerStatus.choices(), default=ContainerStatus.EMPTY)
    coffee_level = models.IntegerField(choices=ContainerStatus.choices(), default=ContainerStatus.EMPTY)
    filter_position = models.BooleanField(default=True)
    mode_value = models.IntegerField(default=0)

    @staticmethod
    def get_stub():
        return products_controller_pb2_grpc.CoffeeMachineControllerStub

    def __str__(self) -> str:
        return self.name

    def get_water_level(self):
        return ContainerStatus(self.water_level).name.title()

    def get_used_water_level(self):
        return ContainerStatus(self.used_water_level).name.title()

    def get_coffee_level(self):
        return ContainerStatus(self.coffee_level).name.title()

    def get_status(self):
        return Status(self.status).name.title()
