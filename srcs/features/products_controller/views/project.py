from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_socio_grpc import generics
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project
from features.products_controller.serializers.project import ProjectSerializer


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"

    model = Project
    template_name = "products_controller/projects/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["product_list"] = BaseProduct.objects.all().filter(project__name=self.object.name)
        except Project.DoesNotExist:
            ...
        return context


class ProjectService(generics.AsyncModelService):
    # https://django-socio-grpc.readthedocs.io/en/stable/features/authentication-permissions.html
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
