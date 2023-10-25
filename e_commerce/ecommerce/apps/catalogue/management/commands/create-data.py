import random

import faker.providers
from django.core.management.base import BaseCommand
from faker import Faker

from ecommerce.apps.catalogue.models import (Category, Product, ProductImage,
                                             ProductType)

CATEGORIES = (  # 15 root categories # "Django models", "DRF", "Django Design Pattenrs",
    "Django",
    "Flask",
    "FastAPI",
    "Pyramid",
    "Bottle",
    "Web2Py",
    "CherryPy",
    "Pycnic",
    "Tornado",
    "Falcon",
    "AIOHTTP",
    "CubicWeb",
    "Dash",
    "Giotto",
    "Grok",
)

PRODUCT_TYPES = (
    "Book",
    "Course",
    "Software",
    "Fonts",
    "Digital art",
    "USB",
    "Floppy disk",
    "Ebook",
    "Computer",
    "Consulting",
    "Video",
    "Website Templates",
    "Email campaign templates",
    "Services",
    "Magazines",
)


class Provider(faker.providers.BaseProvider):
    def ecommerce_category(self):
        return self.random_element(CATEGORIES)

    def ecommerce_product_types(self):
        return self.random_element(PRODUCT_TYPES)


class Command(BaseCommand):
    help = "Command to initially populate your database"

    def handle(self, *args, **kwargs):
        faker = Faker()  # Faker(["pl_PL"]), gdy Ci smutno, gdy Ci źle wygeneruj dane te ;)
        faker.add_provider(Provider)

        for i in range(1, 16):
            c = faker.unique.ecommerce_category()
            pt = faker.unique.ecommerce_product_types()
            title = faker.text(max_nb_chars=25).replace('.', '')

            Category.objects.create(name=c)
            ProductType.objects.create(name=pt)
            Product.objects.create(
                product_type_id=i,
                category_id=i,
                title=title,
                description=faker.text(max_nb_chars=75),
                regular_price=round(random.uniform(15.99, 85.99), 2),
                discount_price=round(random.uniform(8.99, 45.99), 2),
            )
            ProductImage.objects.create(product_id=i, alt_text=faker.text(max_nb_chars=10), is_feature=True)

        check_categories = Category.objects.all().count()
        check_product_types = ProductType.objects.all().count()
        check_products = Product.objects.all().count()

        self.stdout.write(self.style.SUCCESS(f"Number of categories: {check_categories}"))
        self.stdout.write(self.style.SUCCESS(f"Number of product types: {check_product_types}"))
        self.stdout.write(self.style.SUCCESS(f"Number of products: {check_products}"))
