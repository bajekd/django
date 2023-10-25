import json

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone

from .models import Source, Income
from userpreferences.models import UserPreference

# Create your views here.


@login_required(login_url="/authentication/login")
def index(request):
    categories = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {"income": income, "page_obj": page_obj, "currency": currency}

    return render(request, "income/index.html", context)


@login_required(login_url="/authentication/login")
def create_income(request):
    sources = Source.objects.all()
    date = timezone.now()
    context = {"sources": sources, "values": request.POST, "date": date}

    if request.method == "GET":
        return render(request, "income/create_income.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/create_income.html", context)

        description = request.POST["description"]
        date = request.POST["income_date"]
        source = request.POST["source"]

        Income.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            source=source,
            description=description,
        )
        messages.success(request, "Income saved successfully")

        return redirect("income:index")


@login_required(login_url="/authentication/login")
def update_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {"income": income, "values": income, "sources": sources}

    if request.method == "GET":
        return render(request, "income/update_income.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "income/update_income.html", context)

        description = request.POST["description"]
        date = request.POST["income_date"]
        source = request.POST["source"]

        income.amount = amount
        income.date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, "Income updated  successfully")

        return redirect("income:index")


@login_required(login_url="/authentication/login")
def delete_income(request, id):
    income = Income.objects.get(id=id)

    income.delete()
    messages.success(request, "Income removed")

    return redirect("income:index")


def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        income = Income.objects.filter(amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
                date__istartswith=search_str, owner=request.user) | Income.objects.filter(
                description__icontains=search_str, owner=request.user) | Income.objects.filter(
                source__icontains=search_str, owner=request.user)
        data = income.values()

        return JsonResponse(list(data), safe=False)