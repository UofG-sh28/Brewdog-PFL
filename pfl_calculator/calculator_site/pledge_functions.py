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
        """ Replace high carbon fruit and veg (air freight, hot house) for low carbon fruit and veg (local) """
        hcfv_baseline_kg = getattr(self.cf, "fruit_veg_other") / self.conversion_factor["fruit_veg_other"]
        replaced_kg = (hcfv_baseline_kg) * (amount / 100)
        hcfv_carbon = (replaced_kg) * (self.conversion_factor["fruit_veg_other"])
        lcfv_carbon = (replaced_kg) * (self.conversion_factors["fruit_veg_local"])
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
        return indirect_saving(amount)

    def switch_hc_beer_for_lc_beer(self, amount):
        pass

    def switch_bottle_beer_for_kegs(self, amount):
        pass

    def switch_bottle_beer_for_cans(self, amount):
        pass

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
