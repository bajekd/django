from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput

from .models import Address, Customer


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("full_name", "phone_number", "address_line", "town_city", "postal_code", "delivery_instructions")

    def __init__(self, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone_number"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Phone"}
        )
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "City"}
        )
        self.fields["postal_code"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Postal code"}
        )
        self.fields["delivery_instructions"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Specify some instructions if you want"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "login-username",
            }
        )
    )
    password = forms.CharField(
        label="Password",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        ),
    )


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(label="Name", required=True, min_length=4, max_length=100)
    email = forms.EmailField(label="Email", max_length=100, required=True)
    password_1 = forms.CharField(label="Password", min_length=9, widget=PasswordInput, required=True)
    password_2 = forms.CharField(label="Repeat password", min_length=9, widget=PasswordInput, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            "name",
            "email",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Customer with given email already exists!")

        return email

    def clean_password_2(self):
        password_1 = self.cleaned_data["password_1"]
        password_2 = self.cleaned_data["password_2"]
        if password_1 != password_2:
            raise forms.ValidationError("Passwords do not match!")

        return password_2

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control mb-3", "placeholder": "Enter your full name"})
        self.fields["email"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Enter your email", "name": "email", "id": "id_email"}
        )
        self.fields["password_1"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Enter your password"}
        )
        self.fields["password_2"].widget.attrs.update({"class": "form-control", "placeholder": "Repeat your password"})


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "email",
                "id": "form-email",
                "readonly": "readonly",
            }
        ),
    )
    name = forms.CharField(
        label="Name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-3", "placeholder": "Name and surname", "id": "form-username"}
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "name")
