import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, reverse
from paypalcheckoutsdk.orders import OrdersGetRequest

from ecommerce.apps.account.models import Address
from ecommerce.apps.basket.basket import Basket
from ecommerce.apps.orders.models import Order, OrderItem

from .models import DeliveryOptions
from .paypal import PayPalClient

# Create your views here.


@login_required
def delivery_choices(request):
    delivery_options = DeliveryOptions.objects.filter(is_active=True)

    return render(request, "checkout/delivery_choices.html", {"delivery_options": delivery_options})


@login_required
def basket_modify_delivery(request):
    basket = Basket(request)

    if request.POST.get("action") == "POST":
        delivery_option = int(request.POST.get("deliveryOption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_modify_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" in request.session:
            session["purchase"]["delivery_id"] = delivery_type.id
        else:
            session["purchase"] = {"delivery_id": delivery_type.id}
            session.modified = True

    response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
    return response


@login_required
def delivery_address(request):
    session = request.session
    if "purchase" not in session:
        messages.error(request, "Please select delivery option!")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    if not addresses:
        messages.warning(request, "You need to have at least one delivery address!")
        return redirect(reverse("account:addresses"))

    if "address" in session:
        session["address"]["address_id"] = str(addresses[0].id)  # need to be cast into str, if not json throw error
    else:
        session["address"] = {"address_id": str(addresses[0].id)}
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):
    return render(request, "checkout/payment_selection.html")


# PayPal
@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id
    request_order = OrdersGetRequest(data)
    response = PPClient.client.execute(request_order)
    # total_paid = response.result.purchase_units[0].amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()

    return render(request, "checkout/payment_successful.html")
