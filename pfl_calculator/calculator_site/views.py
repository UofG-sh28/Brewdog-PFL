import json
import math
from itertools import chain

from django.shortcuts import render
from calculator_site.forms import CalculatorForm, ActionPlanForm, ActionPlanUtil
from calculator_site.models import Business, CarbonFootprint
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth import logout as lo
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from .forms import RegistrationForm, RegistrationFormStage2, CalculatorUtil
from .models import CarbonFootprint, ActionPlan
from datetime import date

from .pledge_functions import PledgeFunctions

# START UP
static_categories = None
static_scope = None
static_verbose = None
static_action_plan = None


def load_global_data():
    global static_categories
    global static_scope
    global static_verbose
    global static_action_plan

    with open('static/categories.json', encoding='utf8') as cd:
        static_categories = json.load(cd)

    with open("static/verbose.json", encoding='utf8') as verbose:
        static_verbose = json.load(verbose)

    with open('static/scope.json', encoding='utf8') as sd:
        static_scope = json.load(sd)

    with open("static/action_plan_verbose.json", encoding='utf8') as ap_verbose:
        static_action_plan = json.load(ap_verbose)


load_global_data()


# CHECK COOKIE
def check_login(func):
    def inner(request, *args, **kwargs):
        next_url = request.get_full_path()
        # check cookie value
        if request.get_signed_cookie("login", salt="sh28", default=None) == 'yes':
            # if logged in
            return func(request, *args, **kwargs)
        else:
            return redirect('/login/')

    return inner


# INFO PAGES AND HOMEPAGE
def index(request):
    context = {}
    if request.get_signed_cookie("login", salt="sh28", default=None) == 'yes':
        context = {'login': 'yes'}
    return render(request, 'calculator_site/index.html', context)


def outline(request):
    return render(request, 'calculator_site/outline.html')


def scope(request):
    data = Business.objects.all().values()
    context = {'business': data}
    return render(request, 'calculator_site/scope.html', context)


@check_login
# AUTHENTICATED USER PAGES
def dash(request):
    context = {}
    context['login'] = 'yes'
    user = User.objects.get(username=request.user)
    business = Business.objects.get(user=user)
    business_id = business.id
    footprints = CarbonFootprint.objects.filter(business=business)
    carbon_sum = 0
    for footprint in footprints:
        carbon_sum += sum([getattr(footprint, field) for field in CalculatorUtil.retrieve_meta_fields()])
    if carbon_sum <= 0:
        carbon_sum = -500

    context = {'carbon_sum': carbon_sum, 'login': 'yes'}
    return render(request, 'calculator_site/dashboard.html', context)

@check_login
def dash_redirect(request):
    return redirect("/my/dashboard/")


def metrics(request):
    return render(request, 'calculator_site/metrics.html')


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data

@check_login
def report(request):
    user = User.objects.get(username=request.user)
    business = Business.objects.get(user=user)
    footprint = CarbonFootprint.objects.filter(business=business).first()
    data, created= CarbonFootprint.objects.get_or_create(business=business)
    data = to_dict(data)
    if any([getattr(footprint, field) == -1 for field in CalculatorUtil.retrieve_meta_fields()]):
        return render(request, 'calculator_site/pledges.html', context={'cal': 0})

    context = {"id": data["id"], "business_id": data["business"], "year": data["year"]}
    data.pop("year")
    data.pop("business")
    data.pop("id")
    context["json_data"] = mark_safe(json.dumps(str(data)))
    context["cal"] = 1

    # CALCULATE VALUES BY CATEGORY
    carbon_sum = 0
    # GET TOTAL CARBON EMISSIONS
    carbon_sum += sum([data[field] for field in CalculatorUtil.retrieve_meta_fields()])
    carbon_dict = {}
    for cat in static_categories:
        carbon_dict[str(cat)] = {
            "total": 0,
            "percent": 0
        }
        for field in static_categories[cat]:
            #carbon_dict[cat]["total"] += getattr(data[0], field)
            carbon_dict[cat]["total"] += data[field]
        carbon_dict[cat]["percent"] = (carbon_dict[cat]["total"] / carbon_sum) * 100

    # Combine food drink categories.
    carbon_dict["food_drink"]["total"] += carbon_dict["food_drink2"]["total"]
    carbon_dict["food_drink"]["percent"] += carbon_dict["food_drink2"]["percent"]

    # FORMAT THE TOTALS & PERCENTAGES
    for cat in carbon_dict:
        carbon_dict[cat]["total"] = format(carbon_dict[cat]["total"], ".2f")
        carbon_dict[cat]["percent"] = format(carbon_dict[cat]["percent"], ".2f")
        if carbon_dict[cat]["percent"] == "0.00":
            carbon_dict[cat]["percent"] = "<0.01"

    context["carbon_sum"] = format(carbon_sum, ".2f")
    context["carbon_dict"] = carbon_dict

    # CALCULATE VALUES BY SCOPE
    carbon_sum_scope = 0
    # GET TOTAL CARBON EMISSIONS
    carbon_sum_scope += sum([data[field] for field in CalculatorUtil.retrieve_meta_fields()])
    carbon_dict_scope = {}
    for scope in static_scope:
        carbon_dict_scope[str(scope)] = {
            "total": 0,
            "percent": 0
        }
        
        for field in static_scope[scope]:
            carbon_dict_scope[scope]["total"] += data[field]
            
        carbon_dict_scope[scope]["percent"] = (carbon_dict_scope[scope]["total"] / carbon_sum_scope) * 100

    # FORMAT THE TOTALS & PERCENTAGES
    for scope in carbon_dict_scope:
        carbon_dict_scope[scope]["total"] = format(carbon_dict_scope[scope]["total"], ".2f")
        carbon_dict_scope[scope]["percent"] = format(carbon_dict_scope[scope]["percent"], ".2f")
        if carbon_dict_scope[scope]["percent"] == "0.00":
            carbon_dict_scope[scope]["percent"] = "<0.01"

    context["carbon_sum_scope"] = format(carbon_sum_scope, ".2f")
    context["carbon_dict_scope"] = carbon_dict_scope

    context["category_json"] = mark_safe(json.dumps(json.dumps(static_categories)))
    context["scope_json"] = mark_safe(json.dumps(json.dumps(static_scope)))
    return render(request, 'calculator_site/report.html', context=context)

@check_login
def action_plan(request):
    user = User.objects.get(username=request.user)
    business = Business.objects.get(user=user)
    footprints = CarbonFootprint.objects.filter(business=business).first()

    conversion_factors = static_verbose["conversion_factors"]

    pf = PledgeFunctions(footprints, conversion_factors)
    conversion_map = pf.get_func_map()

    ap, _ = ActionPlan.objects.get_or_create(business=business, year=date.today().year)

    pf_mappings = {k: v(getattr(ap, k)) for k, v in conversion_map.items()}

    print(pf_mappings)

    json_data = json.dumps(pf_mappings)

    return render(request, 'calculator_site/action_plan.html', context={"json_data": json_data})

@check_login
def profile(request):
    return render(request, 'calculator_site/profile.html')


def how_it_works(request):
    return render(request, 'calculator_site/how_it_works.html')


# LOGIN AND REGISTER PAGES
def login(request):
    context = {}
    context["error"] = ""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user, password=password)
            if user is not None:
                lg(request, user)
                # set cookie, expire interval 12 hours
                response = redirect('dash')
                response.set_signed_cookie('login', 'yes', salt="sh28", max_age=60 * 60 * 12)
                return response
            else:
                context["error"] = "Incorrect Username or Password"
        else:
            context["error"] = "Incorrect Username or Password"

    if request.user.is_authenticated:
        return dash_redirect(request)

    form = AuthenticationForm()
    context["log_form"] = form
    return render(request, 'calculator_site/login.html', context=context)


@check_login
def logout(request):
    lo(request)
    response = redirect("/")
    response.delete_cookie('login')
    return response


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            lg(request, user)
            return redirect('register2')
        print("Registration Failed")
    form = RegistrationForm()
    return render(request, 'calculator_site/register.html', context={"reg_form": form})


def register2(request):
    if request.method == 'POST':
        form = RegistrationFormStage2(request.POST)
        if form.is_valid():
            form.user = request.user
            form.save()
            print("Registration Completed")
            response = render(request, 'calculator_site/register_success.html')
            response.set_signed_cookie('login', 'yes', salt="sh28", max_age=60 * 60 * 12)
            return response
        print("Registration Failed")
    form = RegistrationFormStage2(user=request.user)
    print(request.user.username)
    return render(request, 'calculator_site/register2.html', context={"reg_form": form})


def about(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        return HttpResponse(request, 'about.html')


class PledgeLoaderView:

    def __init__(self):
        self.verbose = static_verbose
        self.action_plan_verbose = static_action_plan
        self.conversion_factors = static_verbose["conversion_factors"]

        self.action_plan_field_dependencies = {
            "reduce_electricity": ["grid_electricity", "grid_electricity_LOWCARBON"],
            "switch_electricity": ["grid_electricity", "grid_electricity_LOWCARBON"],
            "reduce_gas": ["mains_gas"],
            "reduce_oil": ["oil"],
            "reduce_coal": ["coal"],
            "reduce_wood": ["wood"],
            "energy_audit": [],
            "swap_beef_lamb_for_non_meat": ["beef_lamb"],
            "swap_beef_lamb_for_other_meat": ["beef_lamb"],
            "swap_other_meat_for_non_meat": ["other_meat"],
            "replace_fruit_veg": ["fruit_veg_other"],
            "detailed_menu": [],
            "reduce_food_waste": ["waste_food_landfill", "waste_food_compost", "waste_food_charity"],
            "waste_audit": [],
            "switch_hc_beer_for_lc_beer": ["beer_kegs", "beer_cans", "beer_bottles"],
            "switch_bottle_beer_for_kegs": ["beer_bottles", "beer_bottles_LOWCARBON"],
            "switch_bottle_beer_for_cans": ["beer_bottles", "beer_bottles_LOWCARBON"],
            "switch_canned_beer_for_kegs": ["beer_cans", "beer_cans_LOWCARBON"],
            "reduce_general_waste": ["general_waste_landfill", "general_waste_recycle", "special_waste"],
            "reduce_vehicle_travel_miles": ["goods_delivered_company_owned", "goods_delivered_contracted",
                                            "travel_company_business"],
            "reduce_commuting_miles": ["staff_commuting"],
            "reduce_staff_flights": ["flights_domestic", "flights_international"],
            "reduce_emissions": ["kitchen_equipment_assets", "building_repair_maintenance", "cleaning", "IT_Marketing",
                                 "main_water"],
            "adopt_sustainable_diposable_items": [],
            "sustainably_procure_equipment": [],
        }

    def pledges(self, request):

        if request.method == "POST":
            return self.__pledges_post_request(request)
        elif request.method == "GET":
            return self.__pledges_get_request(request)
        else:
            return HttpResponse("<h1>Error</h1>")

    def __pledges_post_request(self, request):

        # # Parse post data and handle functions
        # # Handle footprint error
        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        footprint, _ = CarbonFootprint.objects.get_or_create(business=business, year=date.today().year)

        data = request.POST

        # Parse post data into python dictionary
        data = dict(data)
        del data["csrfmiddlewaretoken"]

        ap, _ = ActionPlan.objects.get_or_create(business=business, year=date.today().year)

        # save to database
        # TODO
        #  Ensure that all data is within the limits/range
        for k, v in data.items():
            setattr(ap, k, 0 if v[0] == "" else int(v[0]))

        ap.save()

        # redirect to remove pledge page
        repsonse = redirect('/my/action-plan')
        return repsonse

    def __pledges_get_request(self, request):
        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        footprint, _ = CarbonFootprint.objects.get_or_create(business=business, year=date.today().year)

        if any([getattr(footprint, field) == -1 for field in CalculatorUtil.retrieve_meta_fields()]):
            return render(request, 'calculator_site/pledges.html', context={'cal': 0})

        action_plan_form = ActionPlanForm()

        fields = ActionPlanUtil.retrieve_meta_fields()

        colours = self.action_plan_verbose["type-colours"]

        tables = []
        group_fields = []
        table = False
        for field in fields:
            if self.action_plan_verbose[field]["type"] == "Beer" and not table:
                tables.append(PledgeTableWrapper(1, group_fields))
                group_fields = []
                table = True

            pdw = PledgeDataWrapper(field, action_plan_form[field], self.action_plan_verbose[field]["name"],
                                    self.action_plan_verbose[field]["type"],
                                    colours[self.action_plan_verbose[field]["type"]])

            group_fields.append(pdw)
            if all([getattr(footprint, dependency) == 0 for dependency in self.action_plan_field_dependencies[field]
                    if len(dependency) != 0]):
                pdw.applicable = False
                pdw.form.field.disabled = True

        print(group_fields[0].form.field.__dict__)
        tables.append(PledgeTableWrapper(2, group_fields))

        context = {
            "act_plan": tables,
            "cal": 1}
        return render(request, 'calculator_site/pledges.html', context=context)


class PledgeDataWrapper:
    def __init__(self, id, form, name, plan_type, colour):
        self.id = id
        self.form = form
        self.name = name
        self.plan_type = plan_type
        self.colour = colour
        self.applicable = True


class PledgeTableWrapper:
    def __init__(self, column, fields):
        self.column = column
        self.fields = fields

class CalculatorLoaderView:

    # Matching implementation as found in calcualtor.js
    @staticmethod
    def get_decimal_length(r: int) -> int:
        if math.floor(r) == r: return 0
        try:
            return len(str(r).split(".")[1]) or 0
        except Exception:
            return 0

    def __init__(self):
        self.verbose = static_verbose
        self.categories = static_categories

        self.proper_names = self.verbose["fields"]
        self.categories = self.categories
        self.category_names = self.verbose["categories"]
        self.conversion_factors = static_verbose["conversion_factors"]
        
    def calculator(self, request):
        if request.get_signed_cookie("login", salt="sh28", default=None) == 'yes':
            if request.method == "POST":
                return self.__calculator_post_request(request)
            elif request.method == "GET":
                return self.__calculator_get_request(request)
            else:
                return HttpResponse("<h1>Error</h1>")
        else:
            return redirect('/login/')

    def __calculator_post_request(self, request):
        data = request.POST

        # Parse post data into python dictionary
        data = dict(data)
        del data["csrfmiddlewaretoken"]
        # Replacing blanks with default values
        data = {key: 0 if value[0] == "" or value[0] == " " else value[0] for key, value in data.items()}

        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        footprint, _ = CarbonFootprint.objects.get_or_create(business=business, year=date.today().year)

        # TODO
        #  Ensure that all data is within the limits/range
        for k, v in data.items():
            setattr(footprint, k, v)

        footprint.save()

        return self.__calculator_get_request(request)

    def __calculator_get_request(self, request, progress=0):
        # Initialise data fields

        cal_form = CalculatorForm()

        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        footprint, _ = CarbonFootprint.objects.get_or_create(business=business, year=date.today().year)

        category_list = []
        for key, value in self.categories.items():
            field_list = []
            for field_id in value:
                field_list.append(CalculatorDataWrapper(field_id,
                                                        cal_form[field_id], self.proper_names[field_id],
                                                        self.conversion_factors[field_id]))
            category_list.append(CalculatorCategoryWrapper(key, self.category_names[key], field_list))

        # Determine what category to show
        context = {}
        progress = int(request.GET.get('progress', progress))
        # If more than categories redirect to report
        if progress > len(category_list) - 1:
            repsonse = redirect('/my/report')
            return repsonse

        # Handle loading data back into calculator and whether to check applicable
        progress = max(0, progress)
        context["category"] = category_list[progress]
        for cal_data_wrapper in context["category"].fields:
            database_value = getattr(footprint, cal_data_wrapper.id)
            if database_value == -1:
                database_value = " "
            elif database_value == 0:
                cal_data_wrapper.checked = "unchecked"
            else:
                cal_data_wrapper.input_value = f"{round(database_value / cal_data_wrapper.conversion, max(2, self.get_decimal_length(database_value)))} "
            cal_data_wrapper.form.field.initial = database_value

        # Setting all data fields
        context["progress"] = progress + 1
        context["progress_total"] = len(category_list)
        context["progress_complete_range"] = range(progress)
        context["progress_incomplete_range"] = range(len(category_list) - progress - 1)
        context["progress_back"] = progress - 1

        return render(request, 'calculator_site/calculator.html', context=context)


class CalculatorCategoryWrapper:

    def __init__(self, id, name, fields):
        self.id = id
        self.name = name
        self.fields = fields


class CalculatorDataWrapper:

    def __init__(self, field, form, name, conversion):
        self.id = field
        self.form = form
        self.name = name
        self.conversion = conversion
        self.input_value = " "
        self.checked = "checked"
