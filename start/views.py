from django.shortcuts import render


def home(request):
    return render(request, "start/start_page.html")
