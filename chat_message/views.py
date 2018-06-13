from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Messages
from .forms import SendForm


def chat_home(request):
    messages = Messages.objects.all().order_by("-data")

    form = SendForm(request.POST or None)

    if request.POST and form.is_valid():
        new_form = form.save(commit=False)
        new_form.author = request.user
        new_form.save()
        return HttpResponseRedirect(reverse("chat_message:chat_home"))

    context = {
        'messages': messages,
        'form': form
    }

    return render(request, "home/chat_home.html", context)
