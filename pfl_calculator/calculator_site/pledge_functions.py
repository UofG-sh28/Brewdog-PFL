# This file contains the functions used to calculate the percentage of carbon saved on each pledge.
# Each function takes the argument "amount" detailing the percentage that the business has pledged.
from .models import *
from django.contrib.auth.models import User

def reduce_electricity(amount):
    """ Reduce electricity consumption """
    grid_electricity = getattr(cf, "grid_electricity")
    grid_electricity_LOWCARBON = getattr(cf, "grid_electricity_LOWCARBON")
    carbon_saved = (grid_electricity + grid_electricity_LOWCARBON) * (amount/100)
    return carbon_saved

def switch_electricity(amount):
    """ Switch to a high quality 100% renewable electricity supplier (that matches all supply to all customers with 100% renewable power purchase agreements (PPAs).) """
    return

def reduce_gas(amount):
    """ Reduce gas consumption """
    mains_gas = getattr(cf, "mains_gas")
    carbon_saved = (mains_gas) * (amount/100)
    return carbon_saved

def reduce_oil(amount):
    """ Reduce oil consumption """
    oil = getattr(cf, "oil")
    carbon_saved = (oil) * (amount/100)
    return carbon_saved

def reduce_coal(amount):
    """ Reduce coal consumption """
    coal = getattr(cf, "coal")
    carbon_saved = (coal) * (amount/100)
    return carbon_saved

def reduce_wood(amount):
    """ Reduce wood consumption """
    wood = getattr(cf, "wood")
    carbon_saved = (wood) * (amount/100)

def energy_audit(amount):
    if amount != 0:
        return "Indirect Savings"
    else:
        return ""

def swap_beef_lamb_for_non_meat(amount):
    """ Swap beef and lamb for non-animal alternatives """
    beef_lamb = getattr(cf, "beef_lamb")
    carbon_saved = 0
    return carbon_saved

func_map = {
    "reduce_electricity": reduce_electricity,
    "switch_electricity": switch_electricity,
    "reduce_gas": reduce_gas,
    "reduce_oil": reduce_oil,
    "reduce_coal": reduce_coal,
    "reduce_wood": reduce_wood,
    "energy_audit": energy_audit,
    "swap_beef_lamb_for_non_meat": swap_beef_lamb_for_non_meat,
    "swap_beef_lamb_for_other_meat": swap_beef_lamb_for_other_meat,
    "swap_other_meat_for_non_meat": swap_other_meat_for_non_meat,
    "replace_fruit_veg": replace_fruit_veg,
    "detailed_menu": detailed_menu,
    "reduce_food_waste": reduce_food_waste,
    "waste_audit": waste_audit,
    "switch_hc_beer_for_lc_beer": switch_hc_beer_for_lc_beer,
    "switch_bottle_beer_for_kegs": switch_bottle_beer_for_kegs,
    "switch_bottle_beer_for_cans": switch_bottle_beer_for_cans,
    "reduce_general_waste": reduce_general_waste,
    "reduce_vehicle_travel_miles": reduce_vehicle_travel_miles,
    "reduce_commuting_miles": reduce_commuting_miles,
    "reduce_staff_flights": reduce_staff_flights,
    "reduce_emissions": reduce_emissions,
    "adopt_sustainable_diposable_items": adopt_sustainable_diposable_items,
    "sustainably_procure_equipment": sustainably_procure_equipment,
}
