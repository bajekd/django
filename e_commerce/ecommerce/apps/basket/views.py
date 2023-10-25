from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from ecommerce.apps.catalogue.models import Product

from .basket import Basket

# Create your views here.


def basket_summary(request):
    basket = Basket(request)
    return render(request, "basket/summary.html", {"basket": basket})


def basket_ajax_request(request):
    basket = Basket(request)

    if request.POST.get("action") == "POST" or request.POST.get("action") == "PUT":
        product_id = str(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        is_update = True if request.POST.get("action") == "PUT" else False

        product = get_object_or_404(Product, id=product_id)
        basket.modify(product_id=product_id, product=product, qty=product_qty, is_update=is_update)

        basket_qty = basket.__len__()
        basket_subtotal = basket.get_subtotal_price()
        basket_total = basket.get_total_price()

        response = JsonResponse({"qty": basket_qty, "subtotal": basket_subtotal, "total": basket_total})

        return response

    if request.POST.get("action") == "DELETE":
        product_id = str(request.POST.get("productid"))
        # in basket dict, product_id is string, if you will make comparison in basket.delete(), int != str (silly
        # mistake, hard to catch)
        basket.delete(product_id=product_id)

        basket_qty = basket.__len__()
        basket_subtotal = basket.get_subtotal_price()
        basket_total = basket.get_total_price()

        response = JsonResponse({"qty": basket_qty, "subtotal": basket_subtotal, "total": basket_total})

        return response
