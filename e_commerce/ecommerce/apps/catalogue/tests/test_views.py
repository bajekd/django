import pytest
from django.urls import reverse


@pytest.mark.django_db  # required db access to view home page
def test_can_acces_home_page(client):
    url = reverse("catalogue:store_home")

    response = client.get(url)

    assert response.status_code == 200
