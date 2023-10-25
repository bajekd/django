from django.http.response import JsonResponse

from ecommerce.apps.basket.basket import Basket

from .models import Order, OrderItem

# Create your views here.


def add(request):
    basket = Basket(request)
    if request.method == "POST":
        order_key = request.POST.get("order_key")
        user_id = request.user.id
        basket_total = basket.get_total_price()

        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, total_paid=basket_total, order_key=order_key)
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"]
                )

        response = JsonResponse({"success": "Return something"})

        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
