from django.contrib.auth import (
    authenticate,
    login,
    logout,
    )

from django.http import HttpResponseRedirect,Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginForm, RegisterForm, ChangeForm


def account_change_profile(request):
    user = request.user
    form = ChangeForm(request.POST or None)
    if form.is_valid():
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        redirect_to_profile = reverse("accounts:account", kwargs={"id": user.id})
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
        return redirect("/")
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
        return redirect("/")

    context = {
        "form": form,
        'title': title
    }

    return render(request, "home/forms.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")
