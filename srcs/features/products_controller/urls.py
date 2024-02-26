from django.urls import path

from .forms.project import create_project, edit_project
from .views.communication.brightness import BrightnessView
from .views.communication.mode import ModeView
from .views.communication.status import StatusView
from .views.products.base_product import ProductDetailView
from .views.project import ProjectDetailView
from .views.views import IndexView

app_name = "products_controller"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    # projects
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("create_project/", create_project, name="create_project"),
    path("projects/<int:pk>/edit_project/", edit_project, name="edit_project"),
    path("products/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    # product communication functions
    path("products/<int:pk>/status/<str:status>", StatusView.as_view(), name="status_view"),
    path("products/<int:pk>/mode/<str:mode>", ModeView.as_view(), name="mode_view"),
    path("products/<int:pk>/mode/<str:mode>/<int:mode_pk>", ModeView.as_view(), name="mode_view"),
    path("products/<int:pk>/brightness", BrightnessView.as_view(), name="brightness_view"),
]
