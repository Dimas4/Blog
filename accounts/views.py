from django.contrib.auth import (
    authenticate,
    login,
    logout,
    )

from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import (
    LoginForm,
    RegisterForm,
    ChangeForm,
    ChangePassword
    )


def change_password(request):
    form = ChangePassword(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        request.user.set_password(password)
        request.user.save()
        user = authenticate(username=request.user.username, password=request.user.password)
        login(request, user)
        redirect_to_profile = reverse("accounts:account", kwargs={"id": request.user.id})
        return HttpResponseRedirect(redirect_to_profile)

    context = {
        'form': form
    }
    return render(request, "home/change_password.html", context)


def account_change_profile(request):
    form = ChangeForm(request.POST or None)
    if form.is_valid():
        request.user.first_name = form.cleaned_data.get('first_name')
        request.user.last_name = form.cleaned_data.get('last_name')
        request.user.save()
        redirect_to_profile = reverse("accounts:account", kwargs={"id": request.user.id})
        return HttpResponseRedirect(redirect_to_profile)

    context = {
        'form': form
    }
    return render(request, "home/change_profile.html", context)


def account_home(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return HttpResponseRedirect('/')

    context = {
        'user': user
    }
    return render(request, "home/user_account.html", context)


def login_view(request):
    title = "Login"
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse("post:home_page"))
    return render(request, "home/forms.html", {"form": form, "title": title})


def register_view(request):
    title = "Registration"
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect(reverse("post:home_page"))

    context = {
        "form": form,
        'title': title
    }

    return render(request, "home/forms.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")
