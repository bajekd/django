from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
import time


'''from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By'''



class RegisterTest(TestCase):
    @classmethod
    def setUpClass(cls):
        User.objects.all().delete()
        cls.register_url = reverse("authentication:register")
        super().setUpClass()

    def test_can_access_page(self):
        response = self.client.get(RegisterTest.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "authentication/register.html")

    def test_can_register_success(self):
        response = self.client.post(
            RegisterTest.register_url,
            {"username": "test", "email": "test@mail.com", "password": "password123"},
            format="text/html",
        )

        self.assertEqual(response.status_code, 200)

    def test_cant_register_user_with_short_password(self):
        response = self.client.post(
            RegisterTest.register_url,
            {"username": "test", "email": "test@mail.com", "password": "short"},
            format="text/html",
        )

        self.assertEqual(response.status_code, 401)


class LoginTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_url = reverse("authentication:login")
        cls.test_user = User.objects.create_user(
            username="test", email="test@test.com", password="password123"
        )  # this will automaticly set user.is_active = True
        super().setUpClass()

    def test_can_access_page(self):
        response = self.client.get(LoginTest.login_url)

        self.assertTemplateUsed(response, "authentication/login.html")

    def test_can_login_success(self):
        response = self.client.post(
            LoginTest.login_url,
            {"username": "test", "password": "password123"},
            format="text/html",
        )

        self.assertEqual(response.status_code, 302)

    def test_cant_login_with_invalid_credentials(self):
        response = self.client.post(
            LoginTest.login_url,
            {"username": "test", "password": "pass"},
            format="text/html",
        )

        self.assertEqual(response.status_code, 401)

    def test_cant_login_with_unverified_email(self):
        LoginTest.test_user.is_active = False
        LoginTest.test_user.save()
        response = self.client.post(
            LoginTest.login_url,
            {"username": "test", "password": "password123"},
            format="text/html",
        )

        self.assertEqual(response.status_code, 401)

    def test_cant_login_without_all_fields_filled(self):
        response = self.client.post(
            LoginTest.login_url,
            {"username": "test", "password": ""},
            format="text/html",
        )

        self.assertEqual(response.status_code, 401)



class SeleniumRegisterTest(StaticLiveServerTestCase):
    def setUp(self): 
        self.browser = webdriver.Chrome()
        self.register_url = reverse("authentication:register")
        User.objects.create_user(username="test", email='test@test.com')
        #super().setUp()
        
    def tearDown(self):
        self.browser.close()

    
    def test_cant_register_user_with_taken_username(self):
        self.browser.get(f"{self.live_server_url}{self.register_url}")
        username_input_field = self.browser.find_element_by_id("usernameField")

        username_input_field.send_keys("test")
        time.sleep(1)
        p_error_text = self.browser.find_element_by_xpath('/html/body/main/div[1]/div[2]/div/div/form/div[2]/p').text

        self.assertEqual('Sorry username in use, choose another one', p_error_text)

    def test_cant_register_user_with_taken_email(self):
        self.browser.get(f"{self.live_server_url}{self.register_url}")
        email_input_field = self.browser.find_element_by_id("emailField")

        email_input_field.send_keys("test@test.com")
        time.sleep(1)
        p_error_text = self.browser.find_element_by_xpath('/html/body/main/div[1]/div[2]/div/div/form/div[4]/p').text

        self.assertEqual('Sorry email in use, choose another one', p_error_text)

    def test_cant_register_user_with_invalid_email(self):
        self.browser.get(f"{self.live_server_url}{self.register_url}")
        email_input_field = self.browser.find_element_by_id("emailField")

        email_input_field.send_keys("test,com")
        time.sleep(1)
        p_error_text = self.browser.find_element_by_xpath('/html/body/main/div[1]/div[2]/div/div/form/div[4]/p').text

        self.assertEqual('Email is invalid', p_error_text)

        '''timeout = 1
        try:
            expected_element = EC.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/div[2]/div/div/form/div[4]/p'))
            WebDriverWait(self.browser, timeout).until(expected_element)
        except TimeoutException:
            raise('Timed out waiting for expected element to load')''' # --> essentially has the same effect as time.sleep(1), but way more explicit about my actual goal;)