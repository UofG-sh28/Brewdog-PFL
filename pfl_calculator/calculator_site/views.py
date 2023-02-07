import json
import math

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

    context = {'carbon_sum': carbon_sum, 'login': 'yes'}
    return render(request, 'calculator_site/dashboard.html', context)


def dash_redirect(request):
    return redirect("/my/dashboard/")


def metrics(request):
    return render(request, 'calculator_site/metrics.html')


def report(request):
    user = request.user
    business = Business.objects.get_or_create(user=user)[0]
    data = list(CarbonFootprint.objects.get_or_create(business=business))
    context = {"json_data": mark_safe(json.dumps(str(data[0])))}
    with open('static/JS/categories.json') as cd:
        test = json.load(cd)
        context["category_json"] = mark_safe(json.dumps(json.dumps(test)))
    with open('static/JS/scope.json') as sd:
        test = json.load(sd)
        context["scope_json"] = mark_safe(json.dumps(json.dumps(test)))
    return render(request, 'calculator_site/report.html', context)


def action_plan(request):
    return render(request, 'calculator_site/action_plan.html')


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

    form = AuthenticationForm()
    context["log_form"] = form
    return render(request, 'calculator_site/login.html', context=context)


@check_login
def logout(request):
    lo(request)
    response = render(request, 'calculator_site/index.html')
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
            return render(request, 'calculator_site/register_success.html')
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
        file = open("static/JS/verbose.json")
        self.verbose = json.load(file)
        file.close()
        file = open("static/action_plan_verbose.json")
        self.action_plan_verbose = json.load(file)
        file.close()
        self.conversion_factors = self.verbose["conversion_factors"]

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
            setattr(ap, k, int(v[0]))

        ap.save()

        # redirect to remove pledge page
        repsonse = redirect('/my/action_plan')
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
        file = open("static/JS/verbose.json")
        self.verbose = json.load(file)
        file.close()

        file = open("static/JS/categories.json")
        self.categories = json.load(file)
        file.close()

        self.proper_names = self.verbose["fields"]
        self.categories = self.categories
        self.category_names = self.verbose["categories"]
        self.conversion_factors = self.verbose["conversion_factors"]

    def calculator(self, request):

        if request.method == "POST":
            return self.__calculator_post_request(request)
        elif request.method == "GET":
            return self.__calculator_get_request(request)
        else:
            return HttpResponse("<h1>Error</h1>")

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
        context["progress_incomplete_range"] = range(len(category_list) - progress)
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
