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

    file = open("static/verbose.json")
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
        amount_electricity = getattr(self.cf, "grid_electricity") / self.pf.conversion_factor["grid_electricity"]
        replaced_electricity = (amount_electricity) * (50/100)

        replaced_carbon = replaced_electricity * self.pf.conversion_factor["grid_electricity"]
        renewable_carbon = replaced_electricity * self.pf.conversion_factor["grid_electricity_LOWCARBON"]

        carbon_saved = replaced_carbon - renewable_carbon
        self.assertEqual(carbon_saved, self.pf.switch_electricity(50))

    def test_switch_hc_beer_for_lc_beer(self):
        kegs, cans, bottles = getattr(self.cf, "beer_kegs") / self.pf.conversion_factor["beer_kegs"], getattr(self.cf, "beer_cans") / self.pf.conversion_factor["beer_cans"], getattr(self.cf, "beer_bottles") / self.pf.conversion_factor["beer_bottles"]
        total = kegs+cans+bottles

        replaced_litres = total * (96/100)

        avg_hc_conversion_factor = (self.pf.conversion_factor["beer_kegs"] + self.pf.conversion_factor["beer_cans"] + self.pf.conversion_factor["beer_bottles"]) / 3
        avg_lc_conversion_factor = (self.pf.conversion_factor["beer_kegs_LOWCARBON"] + self.pf.conversion_factor["beer_cans_LOWCARBON"] + self.pf.conversion_factor["beer_bottles_LOWCARBON"]) / 3

        amount_hc_beer_carbon = replaced_litres * avg_hc_conversion_factor
        amount_lc_beer_carbon = replaced_litres * avg_lc_conversion_factor

        self.assertEqual(amount_hc_beer_carbon - amount_lc_beer_carbon, self.pf.switch_hc_beer_for_lc_beer(96))

    def test_replace_fruit_veg(self):
        highcarbon_fruit_veg = getattr(self.cf, "fruit_veg_other") / self.pf.conversion_factor["fruit_veg_other"]
        replaced_fruit_veg = highcarbon_fruit_veg * (50/100)

        highcarbon_fruit_veg_carbon = replaced_fruit_veg * self.pf.conversion_factor["fruit_veg_other"]
        lowcarbon_fruit_veg_carbon = replaced_fruit_veg * self.pf.conversion_factor["fruit_veg_local"]

        self.assertEqual(highcarbon_fruit_veg_carbon - lowcarbon_fruit_veg_carbon, self.pf.replace_fruit_veg(50))




class ComplexBeerSwitchTests(TestCase):
    # These tests are a lot more complex so some of the inputs are rounded to account for irrelevant floating point errors
    def setUp(self):
        self.cf, self.pf = test_setup()

    def test_bottles_for_kegs_then_bottles_for_cans(self):
        beer_bottles_ltrs = getattr(self.cf, "beer_bottles") / self.pf.conversion_factor["beer_bottles"]
        beer_bottles_LOWCARBON_ltrs = getattr(self.cf, "beer_bottles_LOWCARBON") / self.pf.conversion_factor["beer_bottles_LOWCARBON"]
        total_ltrs = beer_bottles_ltrs + beer_bottles_LOWCARBON_ltrs

        beer_bottles_conversion_factor = (self.pf.conversion_factor["beer_bottles"] + self.pf.conversion_factor["beer_bottles_LOWCARBON"]) / 2
        beer_kegs_conversion_factor = (self.pf.conversion_factor["beer_kegs"] + self.pf.conversion_factor["beer_kegs_LOWCARBON"]) / 2
        initial_replaced_ltrs = (total_ltrs) * (50 / 100)

        bottle_carbon = initial_replaced_ltrs * beer_bottles_conversion_factor
        keg_carbon = initial_replaced_ltrs * beer_kegs_conversion_factor

        intial_carbon_saved = bottle_carbon - keg_carbon

        secondary_total_ltrs = (beer_bottles_ltrs + beer_bottles_LOWCARBON_ltrs) - initial_replaced_ltrs

        beer_cans_conversion_factor = (self.pf.conversion_factor["beer_cans"] + self.pf.conversion_factor["beer_cans_LOWCARBON"]) / 2
        secondary_replaced_ltrs = (secondary_total_ltrs) * (50 / 100)

        secondary_bottle_carbon = secondary_replaced_ltrs * beer_bottles_conversion_factor
        cans_carbon = secondary_replaced_ltrs * beer_cans_conversion_factor

        expeccted_carbon_saved = int((bottle_carbon - keg_carbon) + (secondary_bottle_carbon - cans_carbon))
        calculated_saved = int(self.pf.switch_bottle_beer_for_kegs(50) + self.pf.switch_bottle_beer_for_cans(50))

        self.assertEqual(expeccted_carbon_saved, calculated_saved)

    def test_ALL_bottles_switched_for_kegs_then_none_for_cans(self):
        beer_bottles_ltrs = getattr(self.cf, "beer_bottles") / self.pf.conversion_factor["beer_bottles"]
        beer_bottles_LOWCARBON_ltrs = getattr(self.cf, "beer_bottles_LOWCARBON") / self.pf.conversion_factor["beer_bottles_LOWCARBON"]
        total_ltrs = beer_bottles_ltrs + beer_bottles_LOWCARBON_ltrs

        beer_bottles_conversion_factor = (self.pf.conversion_factor["beer_bottles"] + self.pf.conversion_factor["beer_bottles_LOWCARBON"]) / 2
        beer_kegs_conversion_factor = (self.pf.conversion_factor["beer_kegs"] + self.pf.conversion_factor["beer_kegs_LOWCARBON"]) / 2
        initial_replaced_ltrs = (total_ltrs) * (100 / 100)

        bottle_carbon = initial_replaced_ltrs * beer_bottles_conversion_factor
        keg_carbon = initial_replaced_ltrs * beer_kegs_conversion_factor

        intial_carbon_saved = bottle_carbon - keg_carbon

        secondary_total_ltrs = (beer_bottles_ltrs + beer_bottles_LOWCARBON_ltrs) - initial_replaced_ltrs

        beer_cans_conversion_factor = (self.pf.conversion_factor["beer_cans"] + self.pf.conversion_factor["beer_cans_LOWCARBON"]) / 2
        secondary_replaced_ltrs = (secondary_total_ltrs) * (50 / 100)

        secondary_bottle_carbon = secondary_replaced_ltrs * beer_bottles_conversion_factor
        cans_carbon = secondary_replaced_ltrs * beer_cans_conversion_factor

        expected_carbon_saved = int((bottle_carbon - keg_carbon))

        calculated_save_1 = self.pf.switch_bottle_beer_for_kegs(100)
        calculated_save_2 = self.pf.switch_bottle_beer_for_cans(100)
        calculated_saved = int(calculated_save_1 + calculated_save_2)

        self.assertEqual(calculated_save_2, 0)
        self.assertEqual(expected_carbon_saved, calculated_saved)

    def test_switch_bottles_for_cans_then_switch_cans_for_kegs(self):
        beer_bottles_ltrs = getattr(self.cf, "beer_bottles") / self.pf.conversion_factor["beer_bottles"]
        beer_bottles_LOWCARBON_ltrs = getattr(self.cf, "beer_bottles_LOWCARBON") / self.pf.conversion_factor["beer_bottles_LOWCARBON"]
        total_ltrs = beer_bottles_ltrs + beer_bottles_LOWCARBON_ltrs + self.pf.beer_bottles_counter

        beer_bottles_conversion_factor = (self.pf.conversion_factor["beer_bottles"] + self.pf.conversion_factor["beer_bottles_LOWCARBON"]) / 2
        beer_cans_conversion_factor = (self.pf.conversion_factor["beer_cans"] + self.pf.conversion_factor["beer_cans_LOWCARBON"]) / 2
        initial_replaced_ltrs = (total_ltrs) * 50/ 100

        bottle_carbon = initial_replaced_ltrs * beer_bottles_conversion_factor
        can_carbon = initial_replaced_ltrs * beer_cans_conversion_factor

        beer_cans_ltrs = getattr(self.cf, "beer_cans") / self.pf.conversion_factor["beer_cans"]
        beer_cans_LOWCARBON_ltrs = getattr(self.cf, "beer_cans_LOWCARBON") / self.pf.conversion_factor["beer_cans_LOWCARBON"]
        initial_plus_bonus_ltrs = beer_cans_ltrs + beer_cans_LOWCARBON_ltrs + initial_replaced_ltrs

        beer_kegs_conversion_factor = (self.pf.conversion_factor["beer_kegs"] + self.pf.conversion_factor["beer_kegs_LOWCARBON"]) / 2
        final_replaced_ltrs = (initial_plus_bonus_ltrs) * (50 / 100)

        bonus_cans_carbon = final_replaced_ltrs * beer_cans_conversion_factor
        keg_carbon = final_replaced_ltrs * beer_kegs_conversion_factor

        expected_carbon_saved = int((bottle_carbon - can_carbon) + (bonus_cans_carbon - keg_carbon))

        calculated_save_1 = self.pf.switch_bottle_beer_for_cans(50)
        calculated_save_2 = self.pf.switch_canned_beer_for_kegs(50)
        calculated_saved = int(calculated_save_1 + calculated_save_2)

        self.assertEqual(expected_carbon_saved, calculated_saved)



class ComplexMeatSwitchTests(TestCase):
    def setUp(self):
        self.cf, self.pf = test_setup()

    def test_switch_all_meat_for_veg_then_none_for_other(self):
        beef_lamb_kg = getattr(self.cf, "beef_lamb") / self.pf.conversion_factor["beef_lamb"]
        replaced_kg = (beef_lamb_kg) * (100 / 100)

        beef_lamb_carbon = replaced_kg * self.pf.conversion_factor["beef_lamb"]
        veg_carbon = replaced_kg * self.pf.conversion_factor["fruit_veg_other"]

        expected_carbon_saved = beef_lamb_carbon - veg_carbon
        actual_carbon_saved = self.pf.swap_beef_lamb_for_non_meat(100) + self.pf.swap_beef_lamb_for_other_meat(50)

        self.assertEqual(expected_carbon_saved, actual_carbon_saved)

    def test_switch_beef_lamb_for_other(self):
        beef_lamb_kg = getattr(self.cf, "beef_lamb") / self.pf.conversion_factor["beef_lamb"]
        replaced_kg = (beef_lamb_kg) * (50 / 100)

        beef_lamb_carbon = replaced_kg * self.pf.conversion_factor["beef_lamb"]
        other_meat_carbon = replaced_kg * self.pf.conversion_factor["other_meat"]

        expected_carbon_saved = beef_lamb_carbon - other_meat_carbon
        actual_carbon_saved = self.pf.swap_beef_lamb_for_other_meat(50)

        self.assertEqual(expected_carbon_saved, actual_carbon_saved)

    def test_beef_lamb_for_other_then_other_for_veg(self):
        beef_lamb_kg = getattr(self.cf, "beef_lamb") / self.pf.conversion_factor["beef_lamb"]
        initial_replaced_kg = (beef_lamb_kg) * (50 / 100)

        beef_lamb_carbon = initial_replaced_kg * self.pf.conversion_factor["beef_lamb"]
        other_meat_carbon = initial_replaced_kg * self.pf.conversion_factor["other_meat"]

        initial_carbon_saved = beef_lamb_carbon - other_meat_carbon

        other_meat_kg = (getattr(self.cf, "other_meat") / self.pf.conversion_factor["other_meat"]) + initial_replaced_kg
        replaced_kg = (other_meat_kg) * (50 / 100)

        veg_carbon = replaced_kg * self.pf.conversion_factor["fruit_veg_other"]
        second_other_meat_saved = replaced_kg * self.pf.conversion_factor["other_meat"]

        secondary_carbon_saved = second_other_meat_saved - veg_carbon

        expected_carbon_saved = initial_carbon_saved + secondary_carbon_saved
        actual_carbon_saved = (self.pf.swap_beef_lamb_for_other_meat(50) + self.pf.swap_other_meat_for_non_meat(50))

        self.assertEqual(expected_carbon_saved, actual_carbon_saved)

class CornerCaseTests(TestCase):
    def setUp(self):
        self.cf, self.pf = test_setup()

    def test_switch_all_electricity(self):
        carbon_saved = self.pf.switch_electricity(100)
        original_carbon = (getattr(self.cf, "grid_electricity"))
        expected_save = (original_carbon / self.pf.conversion_factor["grid_electricity"]) * self.pf.conversion_factor["grid_electricity_LOWCARBON"]

        self.assertEqual(int(original_carbon - expected_save), int(carbon_saved))

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

    def test_indirect(self):
        self.assertEqual("Indirect Savings", self.pf.energy_audit(1))

    def test_no_indirect(self):
        self.assertEqual("", self.pf.energy_audit(0))
