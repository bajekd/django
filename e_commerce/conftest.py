import pytest
from pytest_factoryboy import register

from tests.factories import (AddressFactory, CategoryFactory, CustomerFactory,
                             ProductFactory, ProductSpecificationFactory,
                             ProductSpecificationValueFactory,
                             ProductTypeFactory)

register(CustomerFactory)
register(ProductTypeFactory)
register(ProductSpecificationFactory)
register(ProductFactory)
register(ProductSpecificationValueFactory)
register(CategoryFactory)
register(AddressFactory)


@pytest.fixture
def category(db, category_factory):
    category = category_factory.create()
    # <factory>.create() vs <factory>.build() --> 1) create and save to db, 2) just create --> and this is why we pass
    # db arg to get access to db // alternative use decolator(@pytest.mark.django_db) on given test (aka not here ;))

    return category


@pytest.fixture
def product_type(db, product_type_factory):
    product_type = product_type_factory.create()

    return product_type


@pytest.fixture
def product_specification(db, product_specification_factory):
    product_specification = product_specification_factory.create()

    return product_specification


@pytest.fixture
def product(db, product_factory):
    product = product_factory.create()

    return product


@pytest.fixture
def product_specification_value(db, product_specification_value_factory):
    product_specification_value = product_specification_value_factory.create()

    return product_specification_value


@pytest.fixture
def customer(db, customer_factory):
    customer = customer_factory.create()

    return customer


@pytest.fixture
def admin(db, customer_factory):
    admin = customer_factory.create(name="Admin", is_staff=True, is_superuser=True)

    return admin


@pytest.fixture
def address(db, address_factory):
    address = address_factory.create()

    return address
