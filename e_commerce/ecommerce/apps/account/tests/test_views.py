import pytest
from django.shortcuts import reverse


@pytest.mark.django_db
def test_unregistered_customer_can_access_register_page(client):
    response = client.get(reverse("account:register"))

    assert response.status_code == 200


def test_logged_customer_is_redirected_from_register_page(client, customer):
    client.force_login(customer)

    response = client.get(reverse("account:register"))

    assert response.status_code == 302
