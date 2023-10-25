from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory

from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users


import pdb

# Create your views here.


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            group = Group.objects.get(name="customer")
            user.groups.add(group)

            messages.success(request, f"Account was created for {username}")

            return redirect("login")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, "Username or password is incorrect!")
        else:
            login(request, user)

    return render(request, "accounts/login.html")


@login_required()
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required()
@allowed_users(allowed_roles=["customer"])
def user_page(request):
    return render(request, "accounts/user_page.html")


@login_required()
@allowed_users(allowed_roles=["admin"])
def dashboard(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    delivered_orders = orders.filter(status="Delivered").count()
    pending_orders = orders.filter(status="Pending").count()
    orders = Order.objects.all().order_by("-date_created")[:10]

    customers = Customer.objects.all().order_by("name")

    paginator = Paginator(customers, 10)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)

    context = {
        "orders": orders,
        "total_orders": total_orders,
        "delivered_orders": delivered_orders,
        "pending_orders": pending_orders,
        "paginator": paginator,
        "customers": page_obj,
    }

    return render(request, "accounts/dashboard.html", context)


@login_required()
@allowed_users(allowed_roles=["admin"])
def products(request):
    products = Product.objects.all().order_by("name")

    paginator = Paginator(products, 20)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)

    context = {"products": page_obj, "paginator": paginator}

    return render(request, "accounts/products.html", context)


@login_required()
@allowed_users(allowed_roles=["admin"])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    # Customer.order_set.all(), sort desc by date_created
    orders = Order.objects.filter(customer=pk).order_by("-date_created")
    total_orders = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs

    paginator = Paginator(orders, 15)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)

    context = {
        "customer": customer,
        "paginator": paginator,
        "orders": page_obj,
        "total_orders": total_orders,
        "my_filter": my_filter,
    }

    return render(request, "accounts/customer.html", context)


@login_required()
@allowed_users(allowed_roles=["admin"])
def create_order(request, customer_pk):
    # Parent, Child, child fileds, extra=number of form
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=("product", "status", "note"), extra=10
    )
    customer = Customer.objects.get(id=customer_pk)
    formset = OrderFormSet()

    if request.method == "POST":
        # pass data from POST request and preserve info about given customer (pk)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")

    context = {"form": formset}

    return render(request, "accounts/order_form.html", context)


@login_required()
@allowed_users(allowed_roles=["admin"])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form}

    return render(request, "accounts/order_form.html", context)


@login_required()
@allowed_users(allowed_roles=["admin"])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect("/")

    context = {"item": order}

    return render(request, "accounts/order_deletion.html", context)
