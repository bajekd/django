from decimal import Decimal

from django.conf import settings

from ecommerce.apps.catalogue.models import Product
from ecommerce.apps.checkout.models import DeliveryOptions


class Basket:
    """
    A Basket class providing some default behaviors that can be inherited or overrided, as neccessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def __len__(self):
        """
        Get the basket data and count qty of items
        """

        return sum(item["qty"] for item in self.basket.values())

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for elem in basket.values():
            elem["price"] = Decimal(elem["price"])
            elem["total_price"] = elem["price"] * elem["qty"]
            yield elem

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def modify(self, product_id: str, product: object, qty: int, is_update: bool):
        """
        Adding or/and updating the users basket session data
        """
        if is_update:  # PUT request
            self.basket[product_id]["qty"] = qty
        else:  # POST request
            if product_id in self.basket:
                self.basket[product_id]["qty"] += qty
            else:
                self.basket[product_id] = {"price": str(product.regular_price), "qty": qty}

        self.save()

    def delete(self, product_id):
        """
        Delete item from session data
        """
        product_id = product_id

        if product_id in self.basket:
            del self.basket[product_id]
            try:
                del self.session["address"]
                del self.session["purchase"]
            except Exception:
                pass

            self.save()

    def get_subtotal_price(self):
        return sum(Decimal(elem["price"]) * elem["qty"] for elem in self.basket.values())

    def get_delivery_price(self):
        delivery_price = Decimal(0.00)
        if "purchase" in self.session:
            delivery_price = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return delivery_price

    def basket_modify_delivery(self, delivery_price=0):
        subtotal = self.get_subtotal_price()
        total = subtotal + Decimal(delivery_price)

        return total

    def get_total_price(self):
        subtotal = self.get_subtotal_price()
        delivery_price = self.get_delivery_price()

        total = subtotal + delivery_price

        return total
