from django.urls import path

from .services.communication.brightness import BrightnessView
from .services.communication.mode import ModeView
from .services.communication.status import StatusView

app_name = "products_controller"
urlpatterns = [
    # product communication functions
    path("products/<int:pk>/status/<str:status>", StatusView.as_view(), name="status_view"),
    path("products/<int:pk>/mode/<str:mode>", ModeView.as_view(), name="mode_view"),
    path("products/<int:pk>/mode/<str:mode>/<int:mode_pk>", ModeView.as_view(), name="mode_view"),
    path("products/<int:pk>/brightness", BrightnessView.as_view(), name="brightness_view"),
]
