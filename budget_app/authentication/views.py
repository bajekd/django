import json
from validate_email import validate_email

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import auth
from django.core.mail import EmailMessage
from django.core.mail import send_mail

from .utils import account_activation_token, EmailThread

# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username_error": "username should only contain alphanumeric characters"
                },
                status=400,
            )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "Sorry username in use, choose another one"},
                status=409,
            )

        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse({"email_error": "Email is invalid"}, status=403)
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_error": "Sorry email in use, choose another one"}, status=409
            )

        return JsonResponse({"email_valid": True})


class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        # GET USER DATA
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        context = {"fieldValues": request.POST}

        # VALIDATE
        if not User.objects.filter(username=username, email=email).exists():
            if len(password) < 8:
                messages.add_message(request, messages.ERROR, "Password need to have at least 8 chars")
                return render(request, "authentication/register.html", context, status=401)

            # create a user account
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            email_body = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }
            link = reverse(
                "authentication:activate",
                kwargs={"uidb64": email_body["uid"], "token": email_body["token"]},
            )
            email_subject = "Activate your account"
            activate_url = f"http://{current_site.domain}{link}"

            email = EmailMessage(
                email_subject,
                f"Hi {user.username}, \nPlease click the link below to activate your account \n{activate_url}",
                "blazejdobek94@gmail.com",
                [email],
            )
            EmailThread(email).start()

            messages.success(
                request,
                "Account successfully created! Check your mail to activate your account.",
            )
            return render(request, "authentication/register.html")


class VerificationView(View):
    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)

        if user.is_active:
            return redirect("authentication:login")

        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully")

        return redirect("authentication:login")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        context = {'fieldValues': request.POST}

        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                auth.login(request, user)
                messages.success(request, f'Welcome, {user.username} you are now logged in')
                return redirect('expenses:index')

            messages.error(request, 'Invalid credentials --> try again (or account not activated yet)')
            return render(request, 'authentication/login.html', context, status=401)

        messages.error(request, 'Please fill all fields!')
        return render(request, 'authentication/login.html', context, status=401)


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('authentication:login')