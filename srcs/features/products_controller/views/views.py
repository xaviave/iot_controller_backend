from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from features.products_controller.models.project import Project


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"
    template_name = "products_controller/index.html"
    context_object_name = "latest_projects_list"

    def get_queryset(self):
        try:
            query_data = Project.objects.all().filter(owner=self.request.user).order_by("-pub_date")[:5]
        except Project.DoesNotExist:
            query_data = None
        return query_data
