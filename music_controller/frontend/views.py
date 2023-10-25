from django.shortcuts import render


def index(request):
    return render(request, "frontend/base.html")


def room(request, roomCode):
    return render(request, "frontend/base.html")
