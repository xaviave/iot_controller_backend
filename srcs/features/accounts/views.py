from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UserRegisterForm
from .models import Profile


def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            profile = Profile(user=user, picture=user_form.cleaned_data["picture"])
            profile.save()
            messages.success(request, "Your account has been created!")
            return redirect("/")
    else:
        user_form = UserRegisterForm()
    return render(request, "accounts/register.html", {"user_form": user_form})
