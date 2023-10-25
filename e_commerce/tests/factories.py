import factory
from faker import Faker

from ecommerce.apps.account.models import Address, Customer
from ecommerce.apps.catalogue.models import (Category, Product,
                                             ProductSpecification,
                                             ProductSpecificationValue,
                                             ProductType)

faker = Faker()

# Catalogue


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "django models"


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType
        django_get_or_create = ("name",)

    name = "book"

    # django_get_or_create("field", "other_field", ...)
    # to avoide UNIQUE constraint failed in ProductSpecificationValueFactory --> 1) call subfactory for product, which
    # call subfactory for product_type and 2) call subfactory for specification, which also call subfactory for
    # product_type


class ProductSpecificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecification

    product_type = factory.SubFactory(ProductTypeFactory)
    name = "pages"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_type = factory.SubFactory(ProductTypeFactory)
    category = factory.SubFactory(CategoryFactory)
    title = "product title"
    description = faker.text()
    regular_price = 15.99
    discount_price = 10.99


class ProductSpecificationValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSpecificationValue

    product = factory.SubFactory(ProductFactory)
    specification = factory.SubFactory(ProductSpecificationFactory)
    value = "415"


# Account


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    email = "user@user.com"
    name = "user"
    phone_number = "111 111 111"
    password = "user123"
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(CustomerFactory)
    full_name = faker.name()
    phone_number = faker.phone_number()
    address_line = faker.street_address()
    town_city = faker.city_suffix()
    postal_code = faker.postcode()
