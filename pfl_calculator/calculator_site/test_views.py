from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
import unittest
from django.test import Client
from .forms import *
from .models import *
from django.contrib.auth.models import User


def set_testup():
    test_user = User.objects.create_user(username="pftesting", password="testing")
    Business.objects.create(user=test_user, company_name="pf_tests")
    test_business = Business.objects.get(company_name="pf_tests")
    CarbonFootprint.objects.create(business=test_business, year=2022)
    footprint = CarbonFootprint.objects.get(business=test_business)


class TestDash(TestCase):
    """
        1. visit before login
        2. visit after login
    """
    def setUp(self):
        set_testup()
        self.client = Client()

    def login(self):
        url = '/login/'
        form = {"username": "pftesting", "password": "testing"}
        response = self.client.post(url, form)

    def test_visit_before_login(self):
        url = '/my/dashboard/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_visit_after_login(self):
        self.login()
        url = '/my/dashboard/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/dashboard.html')


class TestLogin(TestCase):
    """
        1. Not existed user
        2. Password incorrect
        3. Login successfully
    """

    def setUp(self):
        set_testup()
        self.client = Client()

    def test_login_success(self):
        url = '/login/'
        form = {"username": "pftesting", "password": "testing"}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/my/dashboard/')

    def test_non_existed_user(self):
        url = '/login/'
        form = {"username": "nouser", "password": "testing"}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Incorrect Username or Password", response.context["error"])

    def test_password_incorrect(self):
        url = '/login/'
        form = {"username": "pftesting", "password": "123"}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Incorrect Username or Password", response.context["error"])


class TestRegister(TestCase):
    """
        1. Password1 is not equal to Password2
        2. Password is too simple
        3. Register successfully
    """

    def setup(self):
        self.client = Client()

    def test_password_not_equal(self):
        url = '/register/'
        form = {'username': 'fred', 'email': '123123123@gmail.com', 'password1': 'abcab123123',
                'password2': '123'}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/register.html')

    def test_password_too_simple(self):
        url = '/register/'
        form = {'username': 'fred', 'email': '123123123@gmail.com', 'password1': '12341234',
                'password2': '12341234'}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/register.html')

    def test_register_success(self):
        url = '/register/'
        form = {'username': 'fred', 'email': '123123123@gmail.com', 'password1': 'abcab123123',
                'password2': 'abcab123123'}
        response = self.client.post(url, form)
        print("registered")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/register/about')


class TestHomePage(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/index.html')


class TestOutline(TestCase):
    def setUp(self):
        self.client = Client()

    def test_outline_page(self):
        response = self.client.get('/outline/')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/outline.html')
