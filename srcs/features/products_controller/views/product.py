from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.products.led.led_panel import LedPanel
from features.products_controller.serializers.products.base_product import (
    BaseProductPolymorphicSerializer,
)
from rest_framework import permissions, viewsets


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"

    model = BaseProduct
    template_name = "products_controller/products/product_detail.html"

    def get_object(self, queryset=None):
        # Retrieve the specific child instance based on the URL
        pk = self.kwargs.get("pk")
        instance = get_object_or_404(BaseProduct, pk=pk)
        self.template_name = instance.html
        return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.__class__ is LedPanel:
            forms = []
            for m in self.object.mode_list:
                forms.append({"model": m.__name__, "form": m.get_form()(), "data": m.objects.all()})
            context["forms"] = forms
        # Add any additional context data if needed
        return context


# views.py


class BaseProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BaseProduct.objects.all()
    serializer_class = BaseProductPolymorphicSerializer
