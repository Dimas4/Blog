from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Count
from django.urls import reverse

from .models import Posts, Category, content_type_queryset
from accounts.models import UserProfile
from comments.forms import CommentForm
from comments.models import Comments
from .forms import FormCreateEdit
from likes.models import Like


User = get_user_model()


def category_view(request):
    categories = Category.objects.all().annotate(count_posts=Count('posts'))
    posts = Posts.objects.filter(category=categories.first()).order_by('-timestamp')
    context = {
        "categories": categories,
        'posts': posts
    }
    return render(request, "home/category_view.html", context)


def add_to_favorite(request, id):
    post = Posts.objects.get(id=id)
    userprofile = UserProfile.objects.get(user=request.user)
    if post in userprofile.favorite_posts.all():
        userprofile.favorite_posts.remove(post)
        return JsonResponse({'key': 1})
    userprofile.favorite_posts.add(post)
    return JsonResponse({'key': 0})


def category_detail_view(request, slug):
    posts = Posts.objects.filter(category__name=slug)

    context = {
        "posts": posts,
        "category": slug
    }

    return render(request, "home/category_detail_view.html", context)


def dynamic_image(request):
    post_id = request.GET.get("post_id")
    new_post = get_object_or_404(Posts, id=post_id)
    data = {
        'post_image': new_post.image.url
    }
    return JsonResponse(data)


def display_posts_by_category(request):
    category = request.GET.get('category_name')
    posts = list(Posts.objects.filter(category__name=category).values('id', 'title', 'image').order_by('-timestamp'))
    data = {
        'posts': posts,
    }
    return JsonResponse(data)


def home_page(request):
    posts = Posts.objects.home()
    path = request.build_absolute_uri('/').strip("/")
    # Posts.objects.aggregate(average_views=Avg('views'))
    popular_posts = Posts.objects.select_related("category", "user").all().order_by('-views')[:3]
    categories = Category.objects.all()[:5]
    path = request.build_absolute_uri('/').strip("/")
    context = {
        'posts': posts,
        'categories': categories,
        'popular_posts': popular_posts,
        'path': path
    }
    return render(request, "home/home_page.html", context)


def add_comment(request):
    content_type = ContentType.objects.get_for_model(Comments)
    post_id = request.POST.get('post_id')
    comment = request.POST.get('comment')
    userprofile = UserProfile.objects.get(user=request.user)
    new_comment = Comments.objects.create(content_type=content_type,
                                          object_id=post_id,
                                          user=request.user,
                                          content=comment,
                                          userprofile=userprofile)

    comment = [{
        'author': new_comment.user.username,
        'comment': new_comment.content,
        'timestamp': new_comment.timestamp.strftime('%Y-%m-%d'),
        'author_image': userprofile.image.url,
        'author_id': new_comment.user.id
    }]

    return JsonResponse(comment, safe=False)


def detail_page(request, id):
    userprofile = UserProfile.objects.get(user=request.user)
    post = Posts.objects.select_related("category", "user").get(id=id)
    content_type = ContentType.objects.get_for_model(Comments)

    form = CommentForm()
    comments = content_type_queryset(model=Comments,
                                     content_type=content_type,
                                     id=id)

    check_like = Posts.is_like(post, request.user)
    check_favorite = Posts.is_favorite(post, request.user)

    post = post.update_view(id)

    context = {
        'post': post,
        'comments': comments,
        'check_like': check_like,
        'check_favorite': check_favorite,
        'form': form
    }

    return render(request, "home/detail_page.html", context)


@login_required
def create_post(request):
    form = FormCreateEdit()

    if request.POST:
        form = FormCreateEdit(request.POST, request.FILES or None)
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
    return render(request, "home/create_post.html", context)


@login_required
def edit_page(request, id):
    post = get_object_or_404(Posts, id=id)

    if request.user != post.user:
        raise Http404

    if request.POST:
        form = FormCreateEdit(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.title = form.cleaned_data.get("title")
            post.content = form.cleaned_data.get("content")
            post.save()
            return HttpResponseRedirect(post.get_absolute_url())

    form = FormCreateEdit()

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
        return JsonResponse({'key': 0})

    model.objects.create(content_type=model_type, object_id=id, user=user)
    return JsonResponse({'key': 1})


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

    elif slug == 'high_rate':
        posts = Posts.objects.high_rate()
        slug1 = "High"
    elif slug == 'middle_rate':
        posts = Posts.objects.middle_rate()
        slug1 = "Middle"
    elif slug == 'low_rate':
        posts = Posts.objects.low_rate()
        slug1 = "Low"

    context = {
        'posts': posts,
        'title': slug1,
    }
    return render(request, "home/choose_rate.html", context)
