from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry
from features.products_controller.views.category import CategoryService
from features.products_controller.views.products.coffee_machine import (
    CoffeeMachineService,
)
from features.products_controller.views.products.led.led_mode import LedModeService
from features.products_controller.views.products.led.led_panel import LedPanelService
from features.products_controller.views.project import ProjectService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("products_controller", server)
    app_registry.register(ProjectService)
    app_registry.register(CategoryService)
    # app_registry.register(BaseProductService)
    app_registry.register(CoffeeMachineService)
    app_registry.register(LedModeService)
    app_registry.register(LedPanelService)
