from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from features.products_controller.models.products.led.led_panel import LedPanel


class CreateLedPanelForm(forms.ModelForm):
    name = forms.CharField(label="Product name", max_length=100)

    class Meta:
        model = LedPanel
        fields = ["name"]


class EditLedPanelForm(forms.ModelForm):
    name = forms.CharField(label="Project name", max_length=100)

    class Meta:
        model = LedPanel
        fields = ["name"]


@login_required
def create_led_panel_form(request):
    if request.method == "POST":
        form = CreateLedPanelForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.pattern = "default"
            obj.color_palette = "default"
            obj.save()
            return redirect("/")
    else:
        form = CreateLedPanelForm()
    return render(request, "products_controller/projects/create_led_panel_form.html", {"form": form})


@login_required
@permission_required("catalog.can_edit")
def edit_project(request, pk):
    project = LedPanel.objects.get(id=pk)

    if request.method == "POST":
        form = EditLedPanelForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("/", pk)
    else:
        form = EditLedPanelForm(instance=project)
    return render(request, "products_controller/projects/edit_led_panel_form.html", {"form": form})
