from django.urls import reverse


def test_category_str(category):
    expected_str = "django models"

    assert category.__str__() == expected_str


def test_category_generate_properly_slug(category):
    expected_slug = "django-models"

    assert category.slug == expected_slug


def test_category_get_absolute_url(client, category):
    expected_url = reverse("catalogue:category_list", args=[category.slug])

    response = client.get(expected_url)

    assert category.get_absolute_url() == expected_url
    assert response.status_code == 200


def test_product_type_str(product_type):
    expected_str = "book"

    assert product_type.__str__() == expected_str


def test_product_specification_str(product_specification):
    expected_str = "pages"

    assert product_specification.__str__() == expected_str


def test_product_str(product):
    expected_str = "product title"

    assert product.__str__() == expected_str


def test_product_generate_properly_slug(product):
    expected_slug = "product-title"

    assert product.slug == expected_slug


def test_product_get_absolute_url(client, product):
    expected_url = reverse("catalogue:product_detail", args=[product.slug])

    response = client.get(expected_url)

    assert product.get_absolute_url() == expected_url
    assert response.status_code == 200


def test_product_specification_value_str(product_specification_value):
    expected_str = "415"

    assert product_specification_value.__str__() == expected_str
