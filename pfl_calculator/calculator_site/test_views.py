from django.test import TestCase
from django.test import Client
from .models import *
from django.contrib.auth.models import User


def set_testup():
    test_user_with_detailed_cf = User.objects.create_user(username="pftesting3", password="testing3")
    Business.objects.create(user=test_user_with_detailed_cf, company_name="pf_tests3")
    test_business = Business.objects.get(company_name="pf_tests3")
    CarbonFootprint.objects.create(business=test_business, year=2023, mains_gas=1, fuel=1, oil=1, coal=1, wood=1,
                                   grid_electricity=1, grid_electricity_LOWCARBON=1, waste_food_landfill=1,
                                   waste_food_compost=1, waste_food_charity=1, bottles_recycle=1,
                                   aluminum_can_recycle=1, general_waste_landfill=1, general_waste_recycle=1,
                                   special_waste=1, goods_delivered_company_owned=1, goods_delivered_contracted=1,
                                   travel_company_business=1, flights_domestic=1, flights_international=1,
                                   staff_commuting=1, beef_lamb=1, other_meat=1, lobster_prawn=1, fin_fish_seafood=1,
                                   milk_yoghurt=1, cheeses=1, fruit_veg_local=1, fruit_veg_other=1, dried_food=1,
                                   beer_kegs=1, beer_cans=1, beer_bottles=1, beer_kegs_LOWCARBON=1,
                                   beer_cans_LOWCARBON=1, beer_bottles_LOWCARBON=1, soft_drinks=1, wine=1, spirits=1,
                                   kitchen_equipment_assets=1, building_repair_maintenance=1, cleaning=1,
                                   IT_Marketing=1, main_water=1, sewage=1)
    ActionPlan.objects.create(business=test_business, year=2023)

    test_user_with_default_cf = User.objects.create_user(username="pftesting2", password="testing2")
    Business.objects.create(user=test_user_with_default_cf, company_name="pf_tests2")
    test_business2 = Business.objects.get(company_name="pf_tests2")
    CarbonFootprint.objects.create(business=test_business2, year=2023)
    ActionPlan.objects.create(business=test_business2, year=2023)

    urls = {
        "login": "/login/",
        "logout": "/logout/",
        "dashboard": "/my/dashboard/",
        "metrics": "/my/metrics",
        "report": "/my/report",
        "action-plan": "/my/pledge-report",
        "register": "/register/",
        "outline": "/outline/",
        "how-it-works": "/how-it-works",
        "mytest": "/my/test"
    }
    return urls


class TestMyPages(TestCase):
    """
        url: /my/dashboard/  /my/metrics  /my/report/ /my/action_plan
        1. visit before login
        2. visit after login
    """

    def setUp(self):
        self.urls = set_testup()
        self.client = Client()

    def login(self, username, password):
        url = self.urls.get("login")
        form = {"username": username, "password": password}
        response = self.client.post(url, form)


    def test_dashboard_visit_after_login(self):
        self.login("pftesting3", "testing3")
        url = self.urls.get("dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/dashboard.html')

    def test_metrics(self):
        self.login("pftesting3", "testing3")
        url = self.urls.get("metrics")
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'calculator_site/metrics.html')

    def test_report_before_login(self):
        url = self.urls.get("report")
        response = self.client.get(url)
        self.assertRedirects(response, self.urls.get("login"))

    def test_report_with_detailed_cf(self):
        self.login("pftesting3", "testing3")
        url = self.urls.get("report")
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'calculator_site/report.html')

    def test_report_with_default_cf(self):
        self.login("pftesting2", "testing2")
        url = self.urls.get("report")
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'calculator_site/report.html')

    def test_action_plan_before_login(self):
        url = self.urls.get("action-plan")
        response = self.client.get(url)
        self.assertRedirects(response, self.urls.get("login"))


    def test_how_it_works(self):
        self.login("pftesting3", "testing3")
        response = self.client.get(self.urls.get("how-it-works"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/how_it_works.html')

    def test_wrong_my_page_after_login(self):
        self.login("pftesting3", "testing3")
        response = self.client.get(self.urls.get("mytest"))
        self.assertRedirects(response, self.urls.get("dashboard"))

    def test_wrong_my_page_before_login(self):
        response = self.client.get(self.urls.get("mytest"))
        self.assertRedirects(response, self.urls.get("login"))


class TestLogin(TestCase):
    """
        url: /login /logout
        1. Not existed user
        2. Password incorrect
        3. Login successfully
    """

    def setUp(self):
        self.urls = set_testup()
        self.client = Client()

    def test_login_success(self):
        url = self.urls.get("login")
        form = {"username": "pftesting2", "password": "testing2"}
        response = self.client.post(url, form)
        self.assertIsNotNone(self.client.cookies['login'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.urls.get("dashboard"))

    def test_non_existed_user(self):
        url = self.urls.get("login")
        form = {"username": "nouser", "password": "testing"}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Incorrect Username or Password", response.context["error"])

    def test_password_incorrect(self):
        url = self.urls.get("login")
        form = {"username": "pftesting", "password": "123"}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertEqual("Incorrect Username or Password", response.context["error"])


class TestRegister(TestCase):
    """
        url: register/  register/about
        1. Password1 is not equal to Password2
        2. Password is too simple
        3. Register successfully
    """

    def setUp(self):
        self.client = Client()
        self.urls = set_testup()

    def test_password_not_equal(self):
        url = self.urls.get("register")
        form = {'username': 'fred', 'email': '123123123@gmail.com', 'password1': 'abcab123123',
                'password2': '123'}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/register.html')

    def test_password_too_simple(self):
        url = self.urls.get("register")
        form = {'username': 'fred', 'email': '123123123@gmail.com', 'password1': '12341234',
                'password2': '12341234'}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/register.html')

    def test_register_success(self):
        url = self.urls.get("register")
        form = {'username': 'fred', 'email': '123123123@gmail.com', 'password1': 'abcab123123',
                'password2': 'abcab123123'}
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/register/about')


class TestHomePage(TestCase):
    """
        url: /
    """

    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/index.html')


class TestOutline(TestCase):
    """
        url: outline/
    """

    def setUp(self):
        self.client = Client()
        self.urls = set_testup()

    def test_outline_page(self):
        response = self.client.get(self.urls.get("outline"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator_site/outline.html')
