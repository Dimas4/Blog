from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Messages
from .forms import SendForm
from accounts.models import UserProfile


def chat_home(request):
    messages = Messages.objects.select_related("author", "author_profile").all()[:15]

    form = SendForm(request.POST or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.author = request.user
        user_profile = get_object_or_404(UserProfile, user=request.user)
        new_form.author_profile = user_profile
        new_form.save()
        return HttpResponseRedirect(reverse("chat_message:chat_home"))

    context = {
        'messages': messages,
        'form': form
    }

    return render(request, "home/chat_home.html", context)
