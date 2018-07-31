from django.contrib.auth import (
    authenticate,
    login,
    logout,
    )
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse


from django.contrib.auth.decorators import login_required
from baskets.models import Basket
from .models import UserProfile
from post.models import Posts
from .forms import (
    LoginForm,
    RegisterForm,
    ChangeForm,
    ChangePassword,
    UploadImage
    )


@login_required
def remove_from_basket(request, id_element):
    post = Posts.objects.get(id=id_element)
    basket = Basket.objects.get(user=request.user).product.remove(post)
    return JsonResponse({'ok': 'ok'})


def change_password(request):
    form = ChangePassword()

    if request.POST:
        form = ChangePassword(request.POST)
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
    return render(request, "accounts/change_password.html", context)


def account_change_profile(request):
    form = ChangeForm()

    if request.POST:
        form = ChangeForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name')
            request.user.last_name = form.cleaned_data.get('last_name')
            request.user.save()

            redirect_to_profile = reverse("accounts:account", kwargs={"id": request.user.id})
            return HttpResponseRedirect(redirect_to_profile)

    context = {
        'form': form
    }
    return render(request, "accounts/change_profile.html", context)


def account_home(request, id):
    user = get_object_or_404(User, id=id)

    baskets = 'False'
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        if basket.exists():
            baskets = basket[0].product.prefetch_related().all()

    userprofile = get_object_or_404(UserProfile, user=user)
    form = UploadImage()

    if request.POST:
        form = UploadImage(request.POST, request.FILES or None)

        if form.is_valid():
            userprofile.image = form.cleaned_data.get("image")
            userprofile.save()
            return HttpResponseRedirect(userprofile.get_user_url())

    favorite_posts = None
    if request.user == user:
        favorite_posts = userprofile.favorite_posts.prefetch_related().all()

    context = {
        'user': user,
        'form': form,
        'userprofile': userprofile,
        'favorite_posts': favorite_posts,
        'baskets': baskets,
        'baskets_len': len(baskets)
    }
    return render(request, "accounts/user_account.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("post:home_page"))

    form = LoginForm()

    title = "Login"
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse("post:home_page"))
            return redirect(reverse("login_view"))

    context = {
        "form": form,
        "title": title
    }

    return render(request, "accounts/login_register_forms.html", context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("post:home_page"))

    title = "Registration"
    form = RegisterForm()

    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            UserProfile.objects.create(user=new_user)
            login(request, new_user)
            return redirect(reverse("post:home_page"))

    context = {
        "form": form,
        'title': title
    }

    return render(request, "accounts/login_register_forms.html", context)


def logout_view(request):
    if request.POST:
        logout(request)
        return redirect("/")
