# This file contains the functions used to calculate the percentage of carbon saved on each pledge.
# Each function takes the argument "amount" detailing the percentage that the business has pledged.
from .models import *
from django.contrib.auth.models import User


class PledgeFunctions:

    def __init__(self, cf):
        self.cf = cf
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
            "reduce_general_waste": self.reduce_general_waste,
            "reduce_vehicle_travel_miles": self.reduce_vehicle_travel_miles,
            "reduce_commuting_miles": self.reduce_commuting_miles,
            "reduce_staff_flights": self.reduce_staff_flights,
            "reduce_emissions": self.reduce_emissions,
            "adopt_sustainable_diposable_items": self.adopt_sustainable_diposable_items,
            "sustainably_procure_equipment": self.sustainably_procure_equipment,
        }

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
        return

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

    def energy_audit(self, amount):
        if amount != 0:
            return "Indirect Savings"
        else:
            return ""

    def swap_beef_lamb_for_non_meat(self, amount):
        """ Swap beef and lamb for non-animal alternatives """
        beef_lamb = getattr(self.cf, "beef_lamb")
        carbon_saved = 0
        return carbon_saved

    def swap_beef_lamb_for_other_meat(self, amount):
        pass

    def swap_other_meat_for_non_meat(self, amount):
        pass

    def replace_fruit_veg(self, amount):
        pass

    def detailed_menu(self, amount):
        pass

    def reduce_food_waste(self, amount):
        pass

    def waste_audit(self, amount):
        pass

    def switch_hc_beer_for_lc_beer(self, amount):
        pass

    def switch_bottle_beer_for_kegs(self, amount):
        pass

    def switch_bottle_beer_for_cans(self, amount):
        pass

    def reduce_general_waste(self, amount):
        pass

    def reduce_vehicle_travel_miles(self, amount):
        pass

    def reduce_commuting_miles(self, amount):
        pass

    def reduce_staff_flights(self, amount):
        pass

    def reduce_emissions(self, amount):
        pass

    def adopt_sustainable_diposable_items(self, amount):
        pass

    def sustainably_procure_equipment(self, amount):
        pass
