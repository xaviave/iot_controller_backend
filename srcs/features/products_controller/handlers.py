from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry
from features.products_controller.services.category import CategoryService
from features.products_controller.services.products.coffee_machine import (
    CoffeeMachineService,
)
from features.products_controller.services.products.led.led_mode import (
    ColorModeService,
    ImageModeService,
    PatternModeService,
    VideoModeService,
)
from features.products_controller.services.products.led.led_panel import LedPanelService
from features.products_controller.services.project import ProjectService
from features.products_controller.services.user import UserService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("products_controller", server)
    app_registry.register(UserService)
    app_registry.register(ProjectService)
    app_registry.register(CategoryService)
    app_registry.register(CoffeeMachineService)
    app_registry.register(LedPanelService)
    app_registry.register(ImageModeService)
    app_registry.register(VideoModeService)
    app_registry.register(ColorModeService)
    app_registry.register(PatternModeService)
