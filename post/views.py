from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.urls import reverse


from comments.forms import CommentForm
from comments.models import Comments
from accounts.models import UserProfile
from .forms import FormCreateEdit, FormTest
from likes.models import Like
from .models import Posts, Category, content_type_queryset
from chat_message.models import Messages


User = get_user_model()


def test_view(request):
    form = FormTest(request.user, request.POST)
    if form.is_valid():
        form.save(request.user)
        return HttpResponseRedirect("/posts/")


    context = {
        "form": form
    }
    return render(request, "home/test_view.html", context)


def category_view(request):
    categories = Category.objects.all().annotate(count_posts=Count('posts'))
    context = {
        "categories": categories,
    }
    return render(request, "home/category_detail.html", context)


def category_detail_view(request, slug):
    posts = Posts.objects.filter(category__name=slug)

    context = {
        "posts": posts,
        "category": slug
    }

    return render(request, "home/category.html", context)


def dynamic_image(request):
    post_id = request.GET.get("post_id")
    new_post = get_object_or_404(Posts, id=post_id)
    data = {
        'post_image': new_post.image.url
    }
    return JsonResponse(data)


def home_page(request):
    posts = Posts.objects.home()
    # Posts.objects.aggregate(average_views=Avg('views'))
    popular_posts = Posts.objects.select_related("category", "user").all().order_by('-views')[:5]
    context = {
        'posts': posts,
        'popular_posts': popular_posts
    }
    return render(request, "home/home_page.html", context)


def detail_page(request, id):
    post = Posts.objects.select_related("category", "user").get(id=id)
    content_type = ContentType.objects.get_for_model(Comments)

    form = CommentForm(request.POST or None)

    if form.is_valid():
        content = form.cleaned_data.get('content')
        userprofile = UserProfile.objects.get(user=request.user)
        Comments.objects.create(content_type=content_type,
                                object_id=id,
                                user=request.user,
                                content=content,
                                userprofile=userprofile)

        return HttpResponseRedirect(post.get_absolute_url())


    comments = content_type_queryset(model=Comments, content_type=content_type, id=id)

    check_like = Posts.is_like(post, request.user)

    post = post.update_view(id)

    context = {
        'post': post,
        'comments': comments,
        'check_like': check_like,
        'form': form
    }

    return render(request, "home/detail_page.html", context)


@login_required
def create_post(request):
    form = FormCreateEdit(request.POST or None, request.FILES or None)
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


@login_required
def edit_page(request, id):
    post = get_object_or_404(Posts, id=id)

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


@login_required
def delete_page(request, id):
    post = get_object_or_404(Posts, id=id)
    if request.user != post.user:
        raise Http404

    if request.POST:
        post.delete()
        return HttpResponseRedirect(reverse("post:home_page"))

    context = {
        'post': post,
    }
    return render(request, "home/delete_page.html", context)


def add_delete_like(model, user, id, model_type, obj, post):
    if obj.exists():
        obj.delete()
        return HttpResponseRedirect(post.get_absolute_url())

    model.objects.create(content_type=model_type, object_id=id, user=user)
    return HttpResponseRedirect(post.get_absolute_url())


@login_required
def like_page(request, id):
    model_type = ContentType.objects.get_for_model(Posts)
    obj = Like.objects.filter(content_type=model_type, object_id=id, user=request.user)
    post = model_type.get_object_for_this_type(id=id)  # or post = Posts.objects.get(id=id)
    user = request.user
    return add_delete_like(Like, user, id, model_type, obj, post)


def high_middle_low_rate(request, slug):
    if slug not in ['high_rate', 'middle_rate', 'low_rate']:
        raise Http404

    if slug == 'high_rate':
        posts = Posts.objects.high_rate()
        slug1 = "High"
    if slug == 'middle_rate':
        posts = Posts.objects.middle_rate()
        slug1 = "Middle"
    if slug == 'low_rate':
        posts = Posts.objects.low_rate()
        slug1 = "Low"

    context = {
        'posts': posts,
        'title': slug1,
    }
    return render(request, "home/choose_rate.html", context)
