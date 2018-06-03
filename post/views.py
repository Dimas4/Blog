from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Posts
from .forms import FormCreateEdit


def home_page(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts
    }
    return render(request, "home/home_page.html", context)


def detail_page(request, id):
    post = Posts.objects.get(id=id)

    post.views = F('views') + 1
    post.save()

    post = Posts.objects.get(id=id)
    context = {
        'post': post
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
