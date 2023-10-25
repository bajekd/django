from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.catalogue.models import Category, Product, ProductType


class TestBasektView(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create(email="admin@admin.com")
        Category.objects.create(name="django", slug="django")
        ProductType.objects.create(name="book")
        Product.objects.create(
            category_id=1,
            title="django beginners",
            slug="django-beginners",
            regular_price="20.05",
            discount_price="15.00",
            product_type_id=1,
        )
        Product.objects.create(
            category_id=1,
            title="django intermediate",
            slug="django-beginners",
            regular_price="20.10",
            discount_price="15.05",
            product_type_id=1,
        )
        Product.objects.create(
            category_id=1,
            title="django advance",
            slug="django-beginners",
            regular_price="20.15",
            discount_price="15.10",
            product_type_id=1,
        )

        self.client.post(
            reverse("basket:basket_ajax_request"),
            {"productid": "1", "productqty": 1, "action": "POST"},
            xhr=True,
        )
        self.client.post(
            reverse("basket:basket_ajax_request"),
            {"productid": "2", "productqty": 2, "action": "POST"},
            xhr=True,
        )

    def test_can_access_basket_summary_url(self):
        response = self.client.get(reverse("basket:basket_summary"))
        self.assertTemplateUsed("basket/summary.html")
        self.assertEqual(response.status_code, 200)

    def test_add_new_item_to_basket(self):
        response = self.client.post(
            reverse("basket:basket_ajax_request"),
            {"productid": "3", "productqty": "3", "action": "POST"},
            xhr=True,
        )

        self.assertEqual(response.json(), {"qty": 6, "subtotal": "120.70", "total": "120.70"})

    def test_add_exists_item_to_basket(self):
        response = self.client.post(
            reverse("basket:basket_ajax_request"),
            {"productid": "2", "productqty": "2", "action": "POST"},
            xhr=True,
        )

        self.assertEqual(response.json(), {"qty": 5, "subtotal": "100.45", "total": "100.45"})

    def test_update_item_in_basket(self):
        response = self.client.post(
            reverse("basket:basket_ajax_request"),
            {"productid": "1", "productqty": "2", "action": "PUT"},
            xhr=True,
        )

        self.assertEqual(response.json(), {"qty": 4, "subtotal": "80.30", "total": "80.30"})

    def test_delete_item_from_basket(self):
        response = self.client.post(
            reverse("basket:basket_ajax_request"), {"productid": "2", "action": "DELETE"}, xhr=True
        )

        self.assertEqual(response.json(), {"qty": 1, "subtotal": "20.05", "total": "20.05"})
