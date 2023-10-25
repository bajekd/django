import pytest


def test_customer_str(customer):
    expected_str = "user"

    assert customer.__str__() == expected_str


def test_superuser_str(admin):
    expected_str = "Admin"

    assert admin.__str__() == expected_str


def test_create_customer_without_email_raise_error(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(email="")

    assert str(err.value) == "You must provide an email address!"


def test_create_customer_with_invalid_email_raise_error(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(email="Abc.aa.com")

    assert str(err.value) == "You must provide a valid email address!"


def test_create_superuser_with_invalid_is_superuser_flag_raise_error(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(is_staff=True, is_superuser=False)

    assert str(err.value) == "Superuser must be assigned to is_superuser=True!"


def test_create_superuser_with_invalid_is_staff_flag_raise_error(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(
            is_staff=False,
            is_superuser=True,
        )

    assert str(err.value) == "Superuser must be assigned to is_staff=True!"


def test_create_superuser_with_invalid_is_active_flag_raise_error(customer_factory):
    with pytest.raises(ValueError) as err:
        customer_factory.create(is_staff=True, is_superuser=True, is_active=False)

    assert str(err.value) == "Superuser must be assigned to is_active=True!"


def test_address_str(address):
    expected_str = f"{address.full_name} Address"

    assert address.__str__() == expected_str
