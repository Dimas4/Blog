from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse
from django.db.models import F
import math

from .forms import FormCreateEdit
from likes.models import Like
from .models import Posts


User = get_user_model()


def home_page(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts
    }
    return render(request, "home/home_page.html", context)


def detail_page(request, id):
    post = Posts.objects.get(id=id)

    check_like = Posts.is_like(post, request.user)

    post.rate = math.ceil(post.likes.count() / post.views)
    post.views = F('views') + 1
    post.save()

    post = Posts.objects.get(id=id)
    context = {
        'post': post,
        'check_like': check_like
    }

    return render(request, "home/detail_page.html", context)


def create_post(request):
    form = FormCreateEdit(request.POST or None)
    if form.is_valid():
        create = form.save(commit=False)
        create.user = request.user
        create.title = form.cleaned_data.get("title")
        create.content = form.cleaned_data.get("content")
        create.save()
        return HttpResponseRedirect(create.get_absolute_url())

    context = {
        'form': form
    }
    return render(request, "home/create_page.html", context)


def edit_page(request, id):
    post = Posts.objects.get(id=id)
    if request.user != post.user:
        raise Http404

    form = FormCreateEdit(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.title = form.cleaned_data.get("title")
        post.content = form.cleaned_data.get("content")
        post.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post': post,
        'form': form
    }
    return render(request, "home/edit_page.html", context)


def delete_page(request, id):
    post = Posts.objects.get(id=id)
    if request.user != post.user:
        raise Http404

    if request.POST:
        post.delete()
        return HttpResponseRedirect(reverse("post:home_page"))

    context = {
        'post': post,
    }
    return render(request, "home/delete_page.html", context)


def add_delete_like(user, id, model_type, obj, post):
    if obj.exists():
        obj.delete()
        return HttpResponseRedirect(post.get_absolute_url())

    Like.objects.create(content_type=model_type, object_id=id, user=user)
    return HttpResponseRedirect(post.get_absolute_url())


def like_page(request, id):
    model_type = ContentType.objects.get_for_model(Posts)
    obj = Like.objects.filter(content_type=model_type, object_id=id, user=request.user)
    post = Posts.objects.get(id=id)
    user = request.user
    return add_delete_like(user, id, model_type, obj, post)


def high_rate(request):
    posts = Posts.objects.high_rate()
    context = {
        'posts': posts,
        'title': 'High rate',
    }
    return render(request, "home/choose_rate.html", context)


def middle_rate(request):
    posts = Posts.objects.middle_rate()
    context = {
        'posts': posts,
        'title': 'Middle rate',
    }
    return render(request, "home/choose_rate.html", context)


def low_rate(request):
    posts = Posts.objects.low_rate()
    context = {
        'posts': posts,
        'title': 'Low rate',
    }
    return render(request, "home/choose_rate.html", context)


