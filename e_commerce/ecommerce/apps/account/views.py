from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from ecommerce.apps.catalogue.models import Product
from ecommerce.apps.orders.views import user_orders

from .forms import RegistrationForm, UserAddressForm, UserEditForm
from .models import Address
from .tokens import account_activation_token


# Create your views here.


def account_register(request):
    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password_2"])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, "account/registration/register_email_confirm.html", {"form": registerForm})

    else:
        registerForm = RegistrationForm()

    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


@login_required
def account_dashboard(request):
    return render(request, "account/dashboard/dashboard.html")


# Orders


@login_required
def orders_dashboard(request):
    orders = user_orders(request)
    return render(request, "account/dashboard/orders.html", {"orders": orders})


@login_required
def edit_details(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/dashboard/edit_details.html", {"user_form": user_form})


@login_required
def delete_user(request):
    user = settings.AUTH_USER_MODEL.get(user_name=request.user.user_name)
    user.is_active = False
    user.save()
    logout(request)

    return redirect("account:delete_confirmation")


# Addresses


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)

    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    address_form = UserAddressForm()

    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = (
                request.user
            )  # address_form.instance.customer = request.user if you perform this on form itself
            address_form.save()

            return redirect(reverse("account:addresses"))

    return render(request, "account/dashboard/edit_address.html", {"form": address_form})


@login_required
def edit_address(request, id):
    address = Address.objects.get(pk=id, customer=request.user)
    address_form = UserAddressForm(instance=address)

    if request.method == "POST":
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()

            return redirect(reverse("account:addresses"))

    return render(request, "account/dashboard/edit_address.html", {"form": address_form})


@login_required
def delete_address(request, id):
    Address.objects.filter(pk=id, customer=request.user).delete()

    return redirect(reverse("account:addresses"))


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(id=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")
    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect(reverse("account:addresses"))


# Wishlist


@login_required
def wishlist_dashboard(request):
    products = Product.objects.filter(users_wishlist=request.user)

    return render(request, "account/dashboard/wishlist.html", {"wishlist": products})


@login_required
def modify_wishlist(request, id):
    product = get_object_or_404(Product, pk=id)

    if product.users_wishlist.filter(pk=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.warning(request, f"Removed {product.title} from your Wishlist.")
    else:
        product.users_wishlist.add(request.user)
        messages.info(request, f"Added {product.title} to your Wishlist.")

    return HttpResponseRedirect(request.META["HTTP_REFERER"])
