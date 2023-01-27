import json
x = '{"id": 1, "business_id": 1, "year": 2022, "mains_gas": 27.06, "fuel": 474.78, "oil": 370.23, "coal": 366.54, "wood": 202.95, "grid_electricity": 38.13, "grid_electricity_LOWCARBON": 9.35, "waste_food_landfill": 77.49, "waste_food_compost": 1.23, "waste_food_charity": 1.23, "bottles_recycle": 2.46, "aluminum_can_recycle": 2.46, "general_waste_landfill": 56.58, "general_waste_recycle": 2.46, "special_waste": 56.58, "goods_delivered_company_owned": 193.11, "goods_delivered_contracted": 193.11, "travel_company_business": 41.82, "flights_domestic": 35.67, "flights_international": 28.29, "staff_commuting": 41.82, "beef_lamb": 2766.27, "other_meat": 1349.31, "lobster_prawn": 2803.17, "fin_fish_seafood": 592.86, "milk_yoghurt": 172.2, "cheeses": 1020.9, "fruit_veg_local": 246.0, "fruit_veg_other": 531.36, "dried_food": 199.26, "beer_kegs": 162.36, "beer_cans": 170.97, "beer_bottles": 179.58, "beer_kegs_LOWCARBON": 86.1, "beer_cans_LOWCARBON": 120.54, "beer_bottles_LOWCARBON": 154.98, "soft_drinks": 79.95, "wine": 158.67, "spirits": 129.15, "kitchen_equipment_assets": 36.9, "building_repair_maintenance": 41.82, "cleaning": 25.83, "IT_Marketing": 14.76, "main_water": 18.45, "sewage": 51.66}'
y = json.loads(x)
print(y[0])


data=list(CarbonFootprint.objects.values())
    json_data = JsonResponse(data,safe=False).content
    context = {"json_data": JsonResponse(data,safe=False).content}