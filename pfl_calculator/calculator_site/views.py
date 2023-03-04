import json
import math
import decimal
from itertools import chain

from django.shortcuts import render
from calculator_site.forms import CalculatorForm, ActionPlanForm, ActionPlanUtil, AdminForm, ChangePasswordForm
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
from .forms import RegistrationForm, RegistrationFormStage2, CalculatorUtil, ChangePasswordForm, FeedbackForm, \
    FeedbackUtil, ActionPlanDetailForm
from .models import CarbonFootprint, ActionPlan, Feedback, ActionPlanDetail
from datetime import date

from .pledge_functions import PledgeFunctions

# START UP
static_categories = None
static_scope = None
static_verbose = None
static_action_plan = None
static_calculator_categories = None
static_feedback_verbose = None


def load_global_data():
    global static_categories
    global static_scope
    global static_verbose
    global static_action_plan
    global static_calculator_categories
    global static_conversion_factors
    global static_feedback_verbose

    with open('static/categories.json', encoding='utf8') as cd:
        static_categories = json.load(cd)

    with open("static/verbose.json", encoding='utf8') as verbose:
        static_verbose = json.load(verbose)

    with open('static/scope.json', encoding='utf8') as sd:
        static_scope = json.load(sd)

    with open("static/action_plan_verbose.json", encoding='utf8') as ap_verbose:
        static_action_plan = json.load(ap_verbose)

    with open("static/calculator_categories.json", encoding='utf8') as cal_cat:
        static_calculator_categories = json.load(cal_cat)

    with open('static/conversion_factors.json', encoding='utf8') as cf:
        static_conversion_factors = json.load(cf)

    with open('static/feedback_verbose.json', encoding='utf8') as fv:
        static_feedback_verbose = json.load(fv)


load_global_data()


# CHECK COOKIE
def check_login(func):
    def inner(request, *args, **kwargs):
        # check cookie value
        if request.get_signed_cookie("login", salt="sh28", default=None) == 'yes':
            # if logged in
            return func(request, *args, **kwargs)
        else:
            response = redirect("/login/")
            response.delete_cookie('login')
            return response

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


class Dashboard:

    def dash(self, request):
        if request.method == "GET":
            return self.__dashboard_get(request)
        elif request.method == "POST":
            return self.__dashboard_post(request)
        else:
            return HttpResponse("<h1> Error </h1>")

    def __dashboard_get(self, request, year=None):
        context = {'login': 'yes'}
        year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)
        if year is not None:
            context["year"] = year
        else:
            context["year"] = year_ck

        user = User.objects.get(username=request.user)
        business = Business.objects.get(user=user)
        business_id = business.id
        footprints = CarbonFootprint.objects.filter(business=business, year=context["year"])
        carbon_sum = 0
        for footprint in footprints:
            carbon_sum += sum([getattr(footprint, field) for field in CalculatorUtil.retrieve_meta_fields()])
        if carbon_sum <= 0:
            carbon_sum = -500
        carbon_sum = format(carbon_sum, ".2f")

        context["years"] = ["2023", "2022", "2021", "2020"]

        context['carbon_sum'] = carbon_sum
        response = render(request, 'calculator_site/dashboard.html', context)
        response.set_signed_cookie('year', context["year"], salt="sh28", max_age=60 * 60 * 12)
        return response

    def __dashboard_post(self, request):
        data = request.POST
        year = data["year_switch"]
        return self.__dashboard_get(request, year)


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
    year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)
    user = User.objects.get(username=request.user)
    business = Business.objects.get(user=user)
    footprint = CarbonFootprint.objects.filter(business=business, year=year_ck).first()
    data, created = CarbonFootprint.objects.get_or_create(business=business, year=year_ck)
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
            # carbon_dict[cat]["total"] += getattr(data[0], field)
            carbon_dict[cat]["total"] += data[field]
        carbon_dict[cat]["percent"] = (carbon_dict[cat]["total"] / carbon_sum) * 100

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
    context["verbose_json"] = mark_safe(json.dumps(json.dumps(static_verbose)))
    return render(request, 'calculator_site/report.html', context=context)


@check_login
def action_plan(request):
    year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)
    user = User.objects.get(username=request.user)
    business = Business.objects.get(user=user)
    footprint = CarbonFootprint.objects.filter(business=business, year=year_ck).first()

    conversion_factors = static_conversion_factors.get(year_ck, None)  # USING STATIC YEAR MUST BE CHANGED

    pf = PledgeFunctions(footprint, conversion_factors)
    conversion_map = pf.get_func_map()

    ap, _ = ActionPlan.objects.get_or_create(business=business, year=year_ck)

    pf_mappings = {k: v(getattr(ap, k)) for k, v in conversion_map.items()}
    ap_values = [getattr(ap, field) for field in ActionPlanUtil.retrieve_meta_fields()]

    print(pf_mappings)

    pledge_savings = sum([value for value in pf_mappings.values() if type(value) != str])

    total_emissions = sum([value for value in ap_values if value != -1])

    #                           Cal percentage

    actual_percent_savings = sum([])

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


def account(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'calculator_site/password_change_success.html')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'calculator_site/account.html', {'form': form})


def staff_dash(request):
    context = {
        "error": None,
        "conversion_factors": static_conversion_factors,
        "form": None
    }
    if (request.user.is_staff):
        print("user")
        if request.method == 'POST':
            form = AdminForm(request.POST)
            if form.is_valid():
                year = form.cleaned_data.get("year")
                form.cleaned_data.pop("year")

                new_data = {}

                for key in form.cleaned_data:
                    new_data[key] = float(form.cleaned_data[key])

                print(new_data)

                if str(year) in static_conversion_factors.keys():
                    # Update
                    print("trying to update")
                    with open('static/conversion_factors.json', "r+", encoding='utf8') as cf:
                        cfs = json.load(cf)

                    cfs[str(year)] = new_data

                    with open('static/conversion_factors.json', "w", encoding='utf8') as cf:
                        json.dump(cfs, cf)
                        cf.write("\n")

                else:
                    # Create
                    print("Trying to insert")
                    with open('static/conversion_factors.json', "r+", encoding='utf8') as cf:
                        cfs = json.load(cf)

                    cfs[str(year)] = new_data

                    with open('static/conversion_factors.json', "w", encoding='utf8') as cf:
                        json.dump(cfs, cf)
                        cf.write("\n")

                load_global_data()
        else:
            form = AdminForm()
            context["form"] = form
            print("set form")
    else:
        context["error"] = "You do not have access to this page."

    print("render")
    return render(request, 'calculator_site/admin_dash.html', context=context)


def admin_report(request):
    context = {
        "conversion_factors": static_conversion_factors,
    }
    if (request.user.is_staff):
        print("user")
    else:
        context["error"] = "You do not have access to this page."
    return render(request, 'calculator_site/admin_report.html', context=context)


class PledgeLoaderView:

    def __init__(self):
        self.verbose = static_verbose
        self.action_plan_verbose = static_action_plan

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
        year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)
        # # Parse post data and handle functions
        # # Handle footprint error
        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        footprint, _ = CarbonFootprint.objects.get_or_create(business=business, year=year_ck)

        data = request.POST

        # Parse post data into python dictionary
        data = dict(data)
        del data["csrfmiddlewaretoken"]

        ap, _ = ActionPlan.objects.get_or_create(business=business, year=year_ck)

        # save to database
        # TODO
        #  Ensure that all data is within the limits/range
        for k, v in data.items():
            setattr(ap, k, 0 if v[0] == "" else int(v[0]))

        ap.save()

        # redirect to remove pledge page
        repsonse = redirect('/my/pledge-report')
        return repsonse

    def __pledges_get_request(self, request):
        year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)
        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        footprint, _ = CarbonFootprint.objects.get_or_create(business=business, year=year_ck)

        if any([getattr(footprint, field) == -1 for field in CalculatorUtil.retrieve_meta_fields()]):
            return render(request, 'calculator_site/pledges.html', context={'cal': 0})

        action_plan_form = ActionPlanForm()

        fields = ActionPlanUtil.retrieve_meta_fields()

        colours = self.action_plan_verbose["type-colours"]

        tables = []
        group_fields = []
        table = False
        default_choice = ((1, "Yes"), (0, "Yes but later"), (0, "Not possible"))
        choices = {
            "switch_electricity": default_choice,
            "detailed_menu": default_choice,
            "waste_audit": default_choice,
            "adopt_sustainable_diposable_items": default_choice,
            "sustainably_procure_equipment": default_choice,
            "energy_audit": default_choice
        }

        for field in fields:
            if self.action_plan_verbose[field]["type"] == "Beer" and not table:
                tables.append(PledgeTableWrapper(1, group_fields))
                group_fields = []
                table = True

            pdw = PledgeDataWrapper(field, action_plan_form[field], self.action_plan_verbose[field]["name"],
                                    self.action_plan_verbose[field]["type"],
                                    colours[self.action_plan_verbose[field]["type"]])

            group_fields.append(pdw)
            if field in choices:
                pdw.form.field.widget.choices = choices.get(field)
            if all([getattr(footprint, dependency) == 0 for dependency in self.action_plan_field_dependencies[field]]) \
                    and len(self.action_plan_field_dependencies[field]) != 0:
                pdw.applicable = False
                pdw.form.field.disabled = True

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
        self.categories = static_calculator_categories

        self.proper_names = self.verbose["fields"]
        self.category_names = self.verbose["categories"]
        self.tooltips = static_verbose["information"]

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
        year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)
        data = request.POST

        # Parse post data into python dictionary
        data = dict(data)
        del data["csrfmiddlewaretoken"]
        # Replacing blanks with default values
        data = {key: 0 if value[0] == "" or value[0] == " " else value[0] for key, value in data.items()}

        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        footprint, _ = CarbonFootprint.objects.get_or_create(business=business, year=year_ck)

        # TODO
        #  Ensure that all data is within the limits/range
        for k, v in data.items():
            setattr(footprint, k, v)

        footprint.save()

        return self.__calculator_get_request(request)

    def __calculator_get_request(self, request, progress=0):
        # Initialise data fields
        year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)

        cal_form = CalculatorForm()

        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        footprint, _ = CarbonFootprint.objects.get_or_create(business=business, year=year_ck)

        category_list = []
        conversion_factors = static_conversion_factors.get(year_ck)
        if conversion_factors is None:
            print("Failed to load conversions factors.")
            return HttpResponse("<h1>Failed to load conversions factors.</h1>")
        for key, value in self.categories.items():
            field_list = []
            for field_id in value:
                field_list.append(CalculatorDataWrapper(field_id,
                                                        cal_form[field_id], self.proper_names[field_id],
                                                        conversion_factors[field_id], self.tooltips[field_id]))
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

    def __init__(self, field, form, name, conversion, tooltip):
        self.id = field
        self.form = form
        self.name = name
        self.conversion = conversion
        self.input_value = " "
        self.checked = "checked"
        self.tooltip = tooltip


class FeedbackDataWrapper:
    def __init__(self, seq, name, form, comment=None):
        self.seq = int(seq / 2 + 1)
        self.name = name
        self.form = form
        self.comment = comment


class FeedbackLoaderView:
    def __init__(self):
        self.feedback_verbose = static_feedback_verbose

    def feedback(self, request):
        if request.method == "POST":
            return self.__feedback_post_request(request)
        elif request.method == "GET":
            return self.__feedback_get_request(request)
        else:
            return HttpResponse("<h1>Error</h1>")

    def __feedback_post_request(self, request):
        user = User.objects.get(username=request.user)
        data = request.POST
        data = dict(data)
        del data["csrfmiddlewaretoken"]
        print(data)
        fb, _ = Feedback.objects.get_or_create(user=user)
        for k, v in data.items():
            setattr(fb, k, v[0])
        fb.save()
        response = redirect('/my/dashboard/')
        return response

    def __feedback_get_request(self, request):
        user = User.objects.get(username=request.user)
        try:
            fb = Feedback.objects.get(user=request.user)
        except Exception as error:
            fb = None

        feedback_form = FeedbackForm()
        fileds = FeedbackUtil.retrieve_meta_fields()

        context = {}
        data = []
        context['feedback_form'] = data
        for index, field in enumerate(fileds):
            if field in self.feedback_verbose.keys():
                if fb is not None:
                    feedback_form.fields[field].widget.attrs.update({"value": getattr(fb, field)})
                    feedback_form.fields[field].initial = getattr(fb, field)
                data.append(FeedbackDataWrapper(index, self.feedback_verbose[field]["name"], feedback_form[field]))
            else:
                dfw = data.pop()
                if fb is not None:
                    feedback_form.fields[field].widget.attrs.update({"value": getattr(fb, field)})
                dfw.comment = feedback_form[field]
                data.append(dfw)

        return render(request, 'calculator_site/feedback.html', context=context)


class ActionPlanDetailDataWrapper:
    def __init__(self, seq, name, form, ownership, start_date, end_date):
        self.seq = seq
        self.name = name
        self.form = form
        self.ownership = ownership
        self.start_date = start_date
        self.end_date = end_date


class ActionPlanDetailLoaderView:
    def __init__(self):
        self.static_action_plan = static_action_plan
        return

    def action_plan_detail(self, request):
        if request.method == "POST":
            return self.__action_plan_detail_post_request(request)
        elif request.method == "GET":
            return self.__action_plan_detail_get_request(request)
        else:
            return HttpResponse("<h1>Error</h1>")

    def __action_plan_detail_post_request(self, request):
        year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)
        user = request.user
        data = request.POST
        data = dict(data)
        del data["csrfmiddlewaretoken"]

        business, _ = Business.objects.get_or_create(user=user)
        apd_list = ActionPlanDetail.objects.filter(business=business, year=year_ck)
        for index, apd in enumerate(apd_list):
            if data["start_date"][index] > data["end_date"][index]:
                return render(request, 'calculator_site/action_plan_detail.html', context={'error':"start date must before end date!"})
            setattr(apd, "ownership", data["ownership"][index])
            setattr(apd, "start_date", data["start_date"][index])
            setattr(apd, "end_date", data["end_date"][index])
            apd.save()
        response = redirect('/my/dashboard/')
        return response

    def __action_plan_detail_get_request(self, request):
        year_ck = request.get_signed_cookie("year", salt="sh28", default=date.today().year)
        # get pledge options
        user = request.user
        business, _ = Business.objects.get_or_create(user=user)
        # check if is ok
        ap = ActionPlan.objects.get(business=business, year=year_ck)
        if ap is None:
            return redirect('/my/pledges')
        # create ActionPlanDetail item
        fields = ActionPlanUtil.retrieve_meta_fields()
        try:
            ap_list = ActionPlanDetail.objects.filter(business=business, year=year_ck)
            if len(ap_list) == 0:
                raise Exception
        except:
            for field in fields:
                value = getattr(ap, field)
                if value != 0:
                    apd = ActionPlanDetail(business=business, year=year_ck, text=field)
                    apd.save()
        # return form
        context = {}
        data = []
        context['action_plan_detail_forms'] = data
        ap_list = ActionPlanDetail.objects.filter(business=business, year=year_ck)
        for index, item in enumerate(ap_list):
            field = getattr(item, "text")
            name = self.static_action_plan[field]["name"]
            acion_plan_detail_form = ActionPlanDetailForm()
            data.append(ActionPlanDetailDataWrapper(index + 1, name, None, acion_plan_detail_form["ownership"],
                                                    acion_plan_detail_form["start_date"],
                                                    acion_plan_detail_form["end_date"]))
        return render(request, 'calculator_site/action_plan_detail.html', context=context)
