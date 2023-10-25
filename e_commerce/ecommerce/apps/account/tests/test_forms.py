import pytest
from django.shortcuts import reverse

from ecommerce.apps.account.forms import RegistrationForm, UserAddressForm


@pytest.mark.parametrize(
    "full_name, phone_number, address_line, town_city, postal_code, delivery_instructions, validity",
    [
        ("Jan Kowalski", "123456789", "ul.Testowa 1A/15", "Testowo", "00-000", "This field can be blank", True),
        ("Jan Kowalski", "123456789", "ul.Testowa 1A/15", "Testowo", "00-000", "", True),
        ("", "123456789", "ul.Testowa 1A/15", "Testowo", "00-000", "", False),
        ("Jan Kowalski", "", "ul.Testowa 1A/15", "Testowo", "00-000", "", False),
        ("Jan Kowalski", "123456789", "", "Testowo", "00-000", "", False),
        ("Jan Kowalski", "123456789", "ul.Testowa 1A/15", "", "00-000", "", False),
        ("Jan Kowalski", "123456789", "ul.Testowa 1A/15", "Testowo", "", "", False),
    ],
)
def test_customer_address_form_correctly_validite_inputs(
    full_name, phone_number, address_line, town_city, postal_code, delivery_instructions, validity
):
    form = UserAddressForm(
        data={
            "full_name": full_name,
            "phone_number": phone_number,
            "address_line": address_line,
            "town_city": town_city,
            "postal_code": postal_code,
            "delivery_instructions": delivery_instructions,
            "validity": validity,
        }
    )

    assert form.is_valid() is validity


def test_customer_after_added_address_is_redirected_to_view_addresses(client, customer):
    client.force_login(customer)
    response = client.post(
        reverse("account:add_address"),
        data={
            "full_name": "test",
            "phone_number": "test",
            "address_line": "test",
            "town_city": "test",
            "postal_code": "test",
            "delivery_instructions": "test",
        },
    )

    assert response.status_code == 302


@pytest.mark.parametrize(
    "name, email, password_1, password_2, validity",
    [
        ("user", "user@user.com", "UseR123456", "UseR123456", True),
        ("", "user@user.com", "UseR123456", "UseR123456", False),  # lack of name
        ("u", "user@user.com", "UseR123456", "UseR123456", False),  # too short name (min_length=4)
        ("user", "", "UseR123456", "UseR123456", False),  # lack of email
        ("user", "user.com", "UseR123456", "UseR123456", False),  # invalid email
        ("user", "user@user.com", "UseR123", "UseR123", False),  # too short password (min_length=9)
        ("user", "user@user.com", "UseR123456", "", False),  # lack of password_2
        ("user", "user@user.com", "UseR12345678", "UseR123456", False),  # mismatch passwords
    ],
)
@pytest.mark.django_db
def test_register_customer_form_correctly_validite_inputs(name, email, password_1, password_2, validity):
    form = RegistrationForm(
        data={
            "name": name,
            "email": email,
            "password_1": password_1,
            "password_2": password_2,
        },
    )

    assert form.is_valid() is validity


@pytest.mark.parametrize(
    "name, email, password_1, password_2",
    [
        (
            "user",
            "user@user.com",
            "",
            "UseR123456",
        ),  # lack of password_1
        (
            "user",
            "user@user.com",
            "UseR123",
            "UseR123456",
        ),  # password_1 is too short
    ],
)
@pytest.mark.django_db
def test_register_customer_form_clean_password_method_raise_key_error_when_no_password_1(
    name, email, password_1, password_2
):
    form = RegistrationForm(
        data={
            "name": name,
            "email": email,
            "password_1": password_1,
            "password_2": password_2,
        },
    )

    with pytest.raises(KeyError) as err:
        form.is_valid()

    assert str(err.value) == "'password_1'"


@pytest.mark.django_db
def test_cant_register_customer_with_taken_email(customer_factory):
    customer_factory.create(email="user@user.com")

    form = RegistrationForm(
        data={
            "name": "User",
            "email": "user@user.com",
            "password_1": "UserPasswD12345",
            "password_2": "UserPasswD12345",
        }
    )

    assert form.is_valid() is False
