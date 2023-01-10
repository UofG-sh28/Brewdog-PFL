from django.test import TestCase
from calculator_site.models import *

# Create your tests here.
def create_test_business():
    user = User(username='test')

    business = Business(
        company_name = "TestBusiness",
        business_address = "Glasgow-ish",
        area_type = "U",
        part_of_world = "UK",
        business_type = "H",
        contact_number = "999",
        business_size = "M"
    )

    return business

def create_test_conversion_factor():
    conversion_factor = ConversionFactor(
        year = 3005,
        mains_gas = 1.5,
        fuel = 1.5,
        oil = 1.5,
        coal = 1.5,
        wood = 1.5,
        grid_electricity = 1.5,
        grid_electricity_LOWCARBON = 1.5,
        waste_food_landfill = 1.5,
        waste_food_compost = 1.5,
        waste_food_charity = 1.5,
        bottles_recycle = 1.5,
        aluminum_can_recycle = 1.5,
        general_waste_landfill = 1.5,
        general_waste_recycle = 1.5,
        special_waste = 1.5,
        goods_delivered_company_owned = 1.5,
        goods_delivered_contracted = 1.5,
        travel_company_business = 1.5,
        flights_domestic = 1.5,
        flights_international = 1.5,
        staff_commuting = 1.5,
        beef_lamb = 1.5,
        other_meat = 1.5,
        lobster_prawn = 1.5,
        fin_fish_seafood = 1.5,
        milk_yoghurt = 1.5,
        cheeses = 1.5,
        fruit_veg_local = 1.5,
        fruit_veg_other = 1.5,
        dried_food = 1.5,
        beer_kegs = 1.5,
        beer_cans = 1.5,
        beer_bottles = 1.5,
        beer_kegs_LOWCARBON = 1.5,
        beer_cans_LOWCARBON = 1.5,
        beer_bottles_LOWCARBON = 1.5,
        soft_drinks = 1.5,
        wine = 1.5,
        spirits = 1.5,
        kitchen_equipment_asssets = 1.5,
        building_repair_maintenance = 1.5,
        cleaning = 1.5,
        IT_Marketing = 1.5,
        main_water = 1.5,
        sewage = 1.5,
    )
    return conversion_factor

class CreateBusiness(TestCase):
    def test_create_business(self):
        business = create_test_business()

class CreateBusinessMetrics(TestCase):
    def test_create_business_metrics(self):
        business = create_test_business()

        business_metrics = BusinessMetrics(
            business = business,
            year = 2023,
            operating_months = 12,
            weekly_openings = 6,
            annual_meals = 12345,
            annual_drinks = 12345,
            annual_customers = 12345,
            revenue = 200000
        )

class CreateConversionFactor(TestCase):
    def test_create_conversion_factor(self):
        cf = create_test_conversion_factor()

class UsageTests(TestCase):
    def test_create_business_usage(self):
        cf = create_test_conversion_factor()
        business = create_test_business()

        business_usage = BusinessUsage(
            business = business,
            conversion_factor = cf,
            year = cf.year,
            mains_gas = 1,
            fuel = 1,
            oil = 1,
            coal = 1,
            wood = 1,
            grid_electricity = 1,
            grid_electricity_LOWCARBON = 1,
            waste_food_landfill = 1,
            waste_food_compost = 1,
            waste_food_charity = 1,
            bottles_recycle = 1,
            aluminum_can_recycle = 1,
            general_waste_landfill = 1,
            general_waste_recycle = 1,
            special_waste = 1,
            goods_delivered_company_owned = 1,
            goods_delivered_contracted = 1,
            travel_company_business = 1,
            flights_domestic = 1,
            flights_international = 1,
            staff_commuting = 1,
            beef_lamb = 1,
            other_meat = 1,
            lobster_prawn = 1,
            fin_fish_seafood = 1,
            milk_yoghurt = 1,
            cheeses = 1,
            fruit_veg_local = 1,
            fruit_veg_other = 1,
            dried_food = 1,
            beer_kegs = 1,
            beer_cans = 1,
            beer_bottles = 1,
            beer_kegs_LOWCARBON = 1,
            beer_cans_LOWCARBON = 1,
            beer_bottles_LOWCARBON = 1,
            soft_drinks = 1,
            wine = 1,
            spirits = 1,
            kitchen_equipment_asssets = 10.00,
            building_repair_maintenance = 10.00,
            cleaning = 10.00,
            IT_Marketing = 10.00,
            main_water = 15,
            sewage = 10.00,
        )
