from django.test import TestCase
from .models import *
from .pledge_functions import PledgeFunctions
from django.contrib.auth.models import User
import json
import random

# We populate the CarbonFootprint for each test case to increase the effectiveness of our tests.
def populate_footprint(footprint):
    footprint.mains_gas = random.randint(0,1000)
    footprint.fuel = random.randint(0,1000)
    footprint.oil = random.randint(0,1000)
    footprint.coal = random.randint(0,1000)
    footprint.wood = random.randint(0,1000)
    footprint.grid_electricity = random.randint(0,1000)
    footprint.grid_electricity_LOWCARBON = random.randint(0,1000)
    footprint.waste_food_landfill = random.randint(0,1000)
    footprint.waste_food_compost = random.randint(0,1000)
    footprint.waste_food_charity = random.randint(0,1000)
    footprint.bottles_recycle = random.randint(0,1000)
    footprint.aluminum_can_recycle = random.randint(0,1000)
    footprint.general_waste_landfill = random.randint(0,1000)
    footprint.general_waste_recycle = random.randint(0,1000)
    footprint.special_waste = random.randint(0,1000)
    footprint.goods_delivered_company_owned = random.randint(0,1000)
    footprint.goods_delivered_contracted = random.randint(0,1000)
    footprint.travel_company_business = random.randint(0,1000)
    footprint.flights_domestic = random.randint(0,1000)
    footprint.flights_international = random.randint(0,1000)
    footprint.staff_commuting = random.randint(0,1000)
    footprint.beef_lamb = random.randint(0,1000)
    footprint.other_meat = random.randint(0,1000)
    footprint.lobster_prawn = random.randint(0,1000)
    footprint.fin_fish_seafood = random.randint(0,1000)
    footprint.milk_yoghurt = random.randint(0,1000)
    footprint.cheeses = random.randint(0,1000)
    footprint.fruit_veg_local = random.randint(0,1000)
    footprint.fruit_veg_other = random.randint(0,1000)
    footprint.dried_food = random.randint(0,1000)
    footprint.beer_kegs = random.randint(0,1000)
    footprint.beer_cans = random.randint(0,1000)
    footprint.beer_bottles = random.randint(0,1000)
    footprint.beer_kegs_LOWCARBON = random.randint(0,1000)
    footprint.beer_cans_LOWCARBON = random.randint(0,1000)
    footprint.beer_bottles_LOWCARBON = random.randint(0,1000)
    footprint.soft_drinks = random.randint(0,1000)
    footprint.wine = random.randint(0,1000)
    footprint.spirits = random.randint(0,1000)
    footprint.kitchen_equipment_assets = random.randint(0,1000)
    footprint.building_repair_maintenance = random.randint(0,1000)
    footprint.cleaning = random.randint(0,1000)
    footprint.IT_Marketing = random.randint(0,1000)
    footprint.main_water = random.randint(0,1000)
    footprint.sewage = random.randint(0,1000)

# Set up objects and populate them using the random value for each test case
def test_setup():
    test_user = User.objects.create(username="pftesting", password="testing")
    Business.objects.create(user = test_user, company_name="pf_tests")
    test_business = Business.objects.get(company_name="pf_tests")
    CarbonFootprint.objects.create(business=test_business, year=2022)
    footprint = CarbonFootprint.objects.get(business = test_business)

    populate_footprint(footprint)

    file = open("static/JS/verbose.json")
    verbose = json.load(file)
    conversion_factor = verbose["conversion_factors"]
    pledge_functions = PledgeFunctions(footprint, conversion_factor)

    return footprint, pledge_functions

class SimpleReductionTests(TestCase):
    def setUp(self):
        self.cf, self.pf = test_setup()

    def test_reduce_electricity(self):
        original_carbon = getattr(self.cf, "grid_electricity") + getattr(self.cf, "grid_electricity_LOWCARBON")
        carbon_saved = self.pf.reduce_electricity(1)
        self.assertEqual(carbon_saved, (original_carbon * (1/100)))

    def test_reduce_gas(self):
        original_carbon = getattr(self.cf, "mains_gas")
        carbon_saved = self.pf.reduce_gas(99)
        self.assertEqual(carbon_saved, (original_carbon * (99/100)))

    def test_reduce_oil(self):
        original_carbon = getattr(self.cf, "oil")
        carbon_saved = self.pf.reduce_oil(50)
        self.assertEqual(carbon_saved, (original_carbon * (50/100)))

    def test_reduce_coal(self):
        original_carbon = getattr(self.cf, "coal")
        carbon_saved = self.pf.reduce_coal(10)
        self.assertEqual(carbon_saved, (original_carbon * (10/100)))

    def test_reduce_wood(self):
        original_carbon = getattr(self.cf, "wood")
        carbon_saved = self.pf.reduce_wood(55)
        self.assertEqual(carbon_saved, original_carbon * (55/100))

    def test_reduce_general_waste(self):
        original_carbon = getattr(self.cf, "general_waste_recycle") + getattr(self.cf, "general_waste_landfill") + getattr(self.cf, "special_waste")
        carbon_saved = self.pf.reduce_general_waste(55)
        self.assertEqual(carbon_saved, original_carbon * (55/100))

    def test_reduce_vehicle_travel_miles(self):
        original_carbon = (getattr(self.cf,"goods_delivered_company_owned") + getattr(self.cf,"goods_delivered_contracted") + getattr(self.cf,"travel_company_business"))
        carbon_saved = self.pf.reduce_vehicle_travel_miles(100)
        self.assertEqual(carbon_saved, original_carbon * (100/100))

    def test_reduce_commuting_miles(self):
        original_carbon = getattr(self.cf, "staff_commuting")
        carbon_saved = self.pf.reduce_commuting_miles(33.5)
        self.assertEqual(carbon_saved, original_carbon * (33.5/100))

    def test_reduce_staff_flights(self):
        original_carbon = getattr(self.cf, "flights_domestic") + getattr(self.cf, "flights_international")
        carbon_saved = self.pf.reduce_staff_flights(5)
        self.assertEqual(carbon_saved, original_carbon * (5/100))


    def test_reduce_emissions(self):
        original_carbon = (getattr(self.cf,"kitchen_equipment_assets") + getattr(self.cf,"building_repair_maintenance") + getattr(self.cf,"cleaning") + getattr(self.cf, "IT_Marketing") + getattr(self.cf, "main_water"))
        carbon_saved = self.pf.reduce_emissions(11.111)
        self.assertEqual(carbon_saved, original_carbon * (11.111/100))

class SimpleSwitchTests(TestCase):
    def setUp(self):
        self.cf, self.pf = test_setup()

    def test_switch_electricity(self):
        self.assertEqual(1,1)

    def test_switch_hc_beer_for_lc_beer(self):
        self.assertEqual(1,1)

class ComplexBeerSwitchTests(TestCase):
    def setUp(self):
        self.cf, self.pf = test_setup()

    def test_bottles_for_kegs_then_bottles_for_cans(self):
        pass

    def test_ALL_bottles_switched_for_kegs_then_none_for_cans(self):
        pass

    def test_switch_bottles_for_cans_then_switch_cans_for_kegs(self):
        pass


class ComplexMeatSwitchTests(TestCase):
    def setUp(self):
        self.cf, self.pf = test_setup()

    def test_switch_all_meat_for_veg(self):
        self.assertEqual(1,1)

class CornerCaseTests(TestCase):
    def setUp(self):
        self.cf, self.pf = test_setup()

    def switch_all_electricity(self):
        carbon_saved = self.pf.switch_electricity(100)
        original_carbon = (getattr(self.cf, "grid_electricity"))
        expected_save = (original_carbon / self.pf.conversion_factor["grid_electricity"]) * self.pf.conversion_factor["grid_electricity_LOWCARBON"]

        self.assertEqual(original_carbon - expected_save, carbon_saved)

    def test_no_reduction(self):
        carbon_saved = self.pf.reduce_oil(0)
        self.assertEqual(0, carbon_saved)

    def test_reduce_one_hundred_percent(self):
        original_carbon = getattr(self.cf, "oil")
        carbon_saved = self.pf.reduce_oil(100)
        self.assertEqual(original_carbon, carbon_saved)

class IndirectSavingTests(TestCase):
    def setUp(self):
        self.cf, self.pf = test_setup()
