from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from main.models import Item
# Create your views here.


def homepage(request):
    return render(request, 'main/home.html')


def itemspage(request):
    if request.method == 'GET':
        items = Item.objects.filter(owner=None)
        return render(request, 'main/items.html', context={'items': items})
    if request.method == 'POST':
        purchased_item = request.POST.get('purchased-item')
        if purchased_item:
            purchased_item_object = Item.objects.get(name=purchased_item)
            purchased_item_object.owner = request.user
            purchased_item_object.save()
            messages.success(
                request, f'Congraturations, you just bought {purchased_item_object.name} for {purchased_item_object.price}.')
    return redirect('items')


def registerpage(request):
    if request.method == 'GET':
        return render(request, 'main/register.html')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, f'You have registered your account successfully. Logged in as {user.username}.')
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('register')


def loginpage(request):
    if request.method == 'GET':
        return render(request, 'main/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f'Hey {user.username}. Good to see you!')
            return redirect('items')
        else:
            messages.error(
                request, f'Given username and password combination is wrong. Try agin or create new account.')
            return redirect('login')


def logoutpage(request):
    logout(request)
    messages.success(request, f'You have logged out. See you next time!')
    return redirect('home')
