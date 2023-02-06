# This file contains the functions used to calculate the percentage of carbon saved on each pledge.
# Each function takes the argument "amount" detailing the percentage that the business has pledged.
from .models import *
from django.contrib.auth.models import User

def indirect_saving(amount):
    if amount != 0:
        return "Indirect Savings"
    else:
        return ""

class PledgeFunctions:

    def __init__(self, cf, conversion_factor):
        self.cf = cf
        self.conversion_factor = conversion_factor
        self.func_map = {
            "reduce_electricity": self.reduce_electricity,
            "switch_electricity": self.switch_electricity,
            "reduce_gas": self.reduce_gas,
            "reduce_oil": self.reduce_oil,
            "reduce_coal": self.reduce_coal,
            "reduce_wood": self.reduce_wood,
            "energy_audit": self.energy_audit,
            "swap_beef_lamb_for_non_meat": self.swap_beef_lamb_for_non_meat,
            "swap_beef_lamb_for_other_meat": self.swap_beef_lamb_for_other_meat,
            "swap_other_meat_for_non_meat": self.swap_other_meat_for_non_meat,
            "replace_fruit_veg": self.replace_fruit_veg,
            "detailed_menu": self.detailed_menu,
            "reduce_food_waste": self.reduce_food_waste,
            "waste_audit": self.waste_audit,
            "switch_hc_beer_for_lc_beer": self.switch_hc_beer_for_lc_beer,
            "switch_bottle_beer_for_kegs": self.switch_bottle_beer_for_kegs,
            "switch_bottle_beer_for_cans": self.switch_bottle_beer_for_cans,
            "switch_canned_beer_for_kegs": self.switch_canned_beer_for_kegs,
            "reduce_general_waste": self.reduce_general_waste,
            "reduce_vehicle_travel_miles": self.reduce_vehicle_travel_miles,
            "reduce_commuting_miles": self.reduce_commuting_miles,
            "reduce_staff_flights": self.reduce_staff_flights,
            "reduce_emissions": self.reduce_emissions,
            "adopt_sustainable_diposable_items": self.adopt_sustainable_diposable_items,
            "sustainably_procure_equipment": self.sustainably_procure_equipment,
        }
        # Counters for complex pledges
        self.beer_bottles_counter = 0
        self.beef_lamb_counter = 0
        self.other_meat_counter = 0
        self.beer_cans_counter = 0




    def get_func_map(self) -> dict:
        return self.func_map

    def reduce_electricity(self, amount):
        """ Reduce electricity consumption """
        grid_electricity = getattr(self.cf, "grid_electricity")
        grid_electricity_LOWCARBON = getattr(self.cf, "grid_electricity_LOWCARBON")
        carbon_saved = (grid_electricity + grid_electricity_LOWCARBON) * (amount / 100)
        return carbon_saved

    def switch_electricity(self, amount):
        """ Switch to a high quality 100% renewable electricity supplier (that matches all supply to all customers with 100% renewable power purchase agreements (PPAs).) """
        grid_electricity_kwh = getattr(self.cf, "grid_electricity") / self.conversion_factor["grid_electricity"]
        replaced_kwh = (grid_electricity_kwh) * (amount / 100)

        grid_co2 = (replaced_kwh) * self.conversion_factor["grid_electricity"]
        renewable_co2 = (replaced_kwh) * self.conversion_factor["grid_electricity_LOWCARBON"]

        carbon_saved = (grid_co2) - (renewable_co2)
        return carbon_saved


    def reduce_gas(self, amount):
        """ Reduce gas consumption """
        mains_gas = getattr(self.cf, "mains_gas")
        carbon_saved = (mains_gas) * (amount / 100)
        return carbon_saved

    def reduce_oil(self, amount):
        """ Reduce oil consumption """
        oil = getattr(self.cf, "oil")
        carbon_saved = (oil) * (amount / 100)
        return carbon_saved

    def reduce_coal(self, amount):
        """ Reduce coal consumption """
        coal = getattr(self.cf, "coal")
        carbon_saved = (coal) * (amount / 100)
        return carbon_saved

    def reduce_wood(self, amount):
        """ Reduce wood consumption """
        wood = getattr(self.cf, "wood")
        carbon_saved = (wood) * (amount / 100)
        return carbon_saved

    def energy_audit(self, amount):
        if amount != 0:
            return "Indirect Savings"
        else:
            return ""


    def swap_beef_lamb_for_non_meat(self, amount):
        """ Swap beef and lamb for non-animal alternatives """
        beef_lamb_kg = getattr(self.cf, "beef_lamb") / self.conversion_factor["beef_lamb"]
        replaced_kg = (beef_lamb_kg) * (amount / 100)
        self.beef_lamb_counter += replaced_kg

        beef_lamb_carbon = replaced_kg * self.conversion_factor["beef_lamb"]
        veg_carbon = replaced_kg * self.conversion_factor["fruit_veg_other"]

        carbon_saved = beef_lamb_carbon - veg_carbon
        return carbon_saved

    def swap_beef_lamb_for_other_meat(self, amount):
        """ Swap beef and lamb for other meat products """
        beef_lamb_kg = (getattr(self.cf, "beef_lamb") / self.conversion_factor["beef_lamb"]) - self.beef_lamb_counter
        replaced_kg = (beef_lamb_kg) * (amount / 100)
        self.other_meat_counter += replaced_kg

        beef_lamb_carbon = replaced_kg * self.conversion_factor["beef_lamb"]
        other_meat_carbon = replaced_kg * self.conversion_factor["other_meat"]

        carbon_saved = beef_lamb_carbon - other_meat_carbon
        return carbon_saved

    def swap_other_meat_for_non_meat(self, amount):
        """ Swap other meats for non-animal alternatives """
        other_meat_kg = (getattr(self.cf, "other_meat") / self.conversion_factor["other_meat"]) +self.other_meat_counter
        replaced_kg = (other_meat_kg) * (amount / 100)

        other_meat_carbon = replaced_kg * self.conversion_factor["other_meat"]
        veg_carbon = replaced_kg * self.conversion_factor["fruit_veg_other"]

        carbon_saved = other_meat_carbon - veg_carbon
        return carbon_saved

    def replace_fruit_veg(self, amount):
        """ Replace high carbon fruit and veg (air freight, hot house) for low carbon fruit and veg (local) """
        hcfv_baseline_kg = getattr(self.cf, "fruit_veg_other") / self.conversion_factor["fruit_veg_other"]
        replaced_kg = (hcfv_baseline_kg) * (amount / 100)
        hcfv_carbon = (replaced_kg) * (self.conversion_factor["fruit_veg_other"])
        lcfv_carbon = (replaced_kg) * (self.conversion_factor["fruit_veg_local"])
        carbon_saved = (hcfv_carbon) - (lcfv_carbon)
        return carbon_saved


    def detailed_menu(self, amount):
        return indirect_saving(amount)

    def reduce_food_waste(self, amount):
        """ Reduce Food Waste """
        total_food_waste = (getattr(self.cf,"waste_food_landfill") + getattr(self.cf,"waste_food_compost") + getattr(self.cf,"waste_food_charity"))
        carbon_saved = (total_food_waste) * (amount / 100)
        return carbon_saved

    def waste_audit(self, amount):
        """ Carry out a waste audit """
        return indirect_saving(amount)

    def switch_hc_beer_for_lc_beer(self, amount):
        """ Switch higher carbon beers to lower carbon beers """
        beer_keg_ltrs = getattr(self.cf, "beer_kegs") / self.conversion_factor["beer_kegs"]
        beer_cans_ltrs = getattr(self.cf, "beer_cans") / self.conversion_factor["beer_cans"]
        beer_bottles_ltrs = getattr(self.cf, "beer_bottles") / self.conversion_factor["beer_bottles"]
        total_ltrs = beer_keg_ltrs + beer_cans_ltrs + beer_bottles_ltrs

        HC_conversion_factor = (self.conversion_factor["beer_kegs"] + self.conversion_factor["beer_cans"] + self.conversion_factor["beer_bottles"]) / 3
        LC_conversion_factor = (self.conversion_factor["beer_kegs_LOWCARBON"] + self.conversion_factor["beer_cans_LOWCARBON"] + self.conversion_factor["beer_bottles_LOWCARBON"]) / 3

        replaced_ltrs = (total_ltrs) * (amount / 100)

        HC_beer_carbon = replaced_ltrs * HC_conversion_factor
        LC_beer_carbon = replaced_ltrs * LC_conversion_factor

        carbon_saved = HC_beer_carbon - LC_beer_carbon
        return carbon_saved



    def switch_bottle_beer_for_kegs(self, amount):
        """ Switch bottled beer to beer from reusable kegs """
        beer_bottles_ltrs = getattr(self.cf, "beer_bottles") / self.conversion_factor["beer_bottles"]
        beer_bottles_LOWCARBON_ltrs = getattr(self.cf, "beer_bottles_LOWCARBON") / self.conversion_factor["beer_bottles_LOWCARBON"]
        total_ltrs = beer_bottles_ltrs + beer_bottles_LOWCARBON_ltrs

        beer_bottles_conversion_factor = (self.conversion_factor["beer_bottles"] + self.conversion_factor["beer_bottles_LOWCARBON"]) / 2
        beer_kegs_conversion_factor = (self.conversion_factor["beer_kegs"] + self.conversion_factor["beer_kegs_LOWCARBON"]) / 2
        replaced_ltrs = (total_ltrs) * (amount / 100)

        self.beer_bottles_counter += replaced_ltrs

        bottle_carbon = replaced_ltrs * beer_bottles_conversion_factor
        keg_carbon = replaced_ltrs * beer_kegs_conversion_factor

        carbon_saved = bottle_carbon - keg_carbon
        return carbon_saved

    def switch_bottle_beer_for_cans(self, amount):
        """ Switch bottled beer to canned beer """
        beer_bottles_ltrs = getattr(self.cf, "beer_bottles") / self.conversion_factor["beer_bottles"]
        beer_bottles_LOWCARBON_ltrs = getattr(self.cf, "beer_bottles_LOWCARBON") / self.conversion_factor["beer_bottles_LOWCARBON"]
        total_ltrs = (beer_bottles_ltrs + beer_bottles_LOWCARBON_ltrs) - self.beer_bottles_counter

        beer_bottles_conversion_factor = (self.conversion_factor["beer_bottles"] + self.conversion_factor["beer_bottles_LOWCARBON"]) / 2
        beer_cans_conversion_factor = (self.conversion_factor["beer_cans"] + self.conversion_factor["beer_cans_LOWCARBON"]) / 2
        replaced_ltrs = (total_ltrs) * (amount / 100)

        self.beer_cans_counter += replaced_ltrs

        bottle_carbon = replaced_ltrs * beer_bottles_conversion_factor
        cans_carbon = replaced_ltrs * beer_cans_conversion_factor

        carbon_saved = bottle_carbon - cans_carbon
        return carbon_saved

    def switch_canned_beer_for_kegs(self, amount):
        """ Switch our canned beer to beer from reusable kegs """
        beer_cans_ltrs = getattr(self.cf, "beer_cans") / self.conversion_factor["beer_cans"]
        beer_cans_LOWCARBON_ltrs = getattr(self.cf, "beer_cans_LOWCARBON") / self.conversion_factor["beer_cans_LOWCARBON"]
        total_ltrs = beer_cans_ltrs + beer_cans_LOWCARBON_ltrs + self.beer_cans_counter

        beer_cans_conversion_factor = (self.conversion_factor["beer_cans"] + self.conversion_factor["beer_cans_LOWCARBON"]) / 2
        beer_kegs_conversion_factor = (self.conversion_factor["beer_kegs"] + self.conversion_factor["beer_kegs_LOWCARBON"]) / 2
        replaced_ltrs = (total_ltrs) * (amount / 100)

        cans_carbon = replaced_ltrs * beer_cans_conversion_factor
        keg_carbon = replaced_ltrs * beer_kegs_conversion_factor

        carbon_saved = cans_carbon - keg_carbon
        return carbon_saved

    def reduce_general_waste(self, amount):
        """ Reduce general waste """
        total_general_waste = (getattr(self.cf,"general_waste_landfill") + getattr(self.cf,"general_waste_recycle") + getattr(self.cf,"special_waste"))
        carbon_saved = (total_general_waste) * (amount / 100)
        return carbon_saved

    def reduce_vehicle_travel_miles(self, amount):
        """ Reduce vehicle road miles (companny travel and deliveries) """
        total_vehicle_travel_miles = (getattr(self.cf,"goods_delivered_company_owned") + getattr(self.cf,"goods_delivered_contracted") + getattr(self.cf,"travel_company_business"))
        carbon_saved = (total_vehicle_travel_miles * (amount / 100))
        return carbon_saved

    def reduce_commuting_miles(self, amount):
        """ Reduce commuting vehicle road miles """
        staff_commuting = getattr(self.cf, "staff_commuting")
        carbon_saved = (staff_commuting) * (amount / 100)
        return carbon_saved

    def reduce_staff_flights(self, amount):
        """ Reduce staff flights """
        total_staff_flights = (getattr(self.cf, "flights_domestic") + getattr(self.cf, "flights_international"))
        carbon_saved = (total_staff_flights) * (amount / 100)
        return carbon_saved

    def reduce_emissions(self, amount):
        """ Reduce emissions from Operations and Maintenance """
        total_emissions = (getattr(self.cf,"kitchen_equipment_assets") + getattr(self.cf,"building_repair_maintenance") + getattr(self.cf,"cleaning") + getattr(self.cf, "IT_Marketing") + getattr(self.cf, "main_water"))
        carbon_saved = (total_emissions) * (amount / 100)
        return carbon_saved

    def adopt_sustainable_diposable_items(self, amount):
        """ Adopt sustainable purchasing of non-food disposable items """
        return indirect_saving(amount)

    def sustainably_procure_equipment(self, amount):
        """ Sustainable procurement of equipment and furniture: where possbile, buy pre-loved """
        return indirect_saving(amount)
