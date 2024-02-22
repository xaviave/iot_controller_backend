from datetime import datetime

from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from features.products_controller.models.products.base_product import BaseProduct
from features.products_controller.models.project import Project


class CreateProjectForm(forms.ModelForm):
    name = forms.CharField(label="Project name", max_length=100)
    products = forms.ModelMultipleChoiceField(
        queryset=BaseProduct.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = ["name", "products"]


class EditProjectForm(forms.ModelForm):
    name = forms.CharField(label="Project name", max_length=100)
    products = forms.ModelMultipleChoiceField(
        queryset=BaseProduct.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = ["name", "products"]


@login_required
def create_project(request):
    print(request.user.picture)
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            obj.owner = request.user
            obj.pub_date = datetime.now()
            obj.save()
            return redirect("/")
    else:
        form = CreateProjectForm()
    return render(request, "products_controller/projects/create_project.html", {"form": form})


@login_required
@permission_required("catalog.can_edit")
def edit_project(request, pk):
    project = Project.objects.get(id=pk)

    if request.method == "POST":
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("/", pk)
    else:
        form = EditProjectForm(instance=project)
    return render(request, "products_controller/projects/edit_project.html", {"form": form})
