import json

from django.shortcuts import render
from calculator_site.forms import CalculatorForm
from calculator_site.models import Business, CarbonFootprint
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth import logout as lo
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from  django.utils.safestring import mark_safe
from .forms import RegistrationForm
from .models import CarbonFootprint
from .pledge_functions import PledgeFunctions


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
    return render(request, 'calculator_site/dashboard.html', context)


def metrics(request):
    return render(request, 'calculator_site/metrics.html')


def report(request):
    data = list(CarbonFootprint.objects.all().values())
    context = {"json_data": mark_safe(json.dumps(str(data[0])))}
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
    return render(request, 'calculator_site/register.html', context={"reg_form":form})

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
    return render(request, 'calculator_site/register2.html', context={"reg_form":form})

def about(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        return HttpResponse(request, 'about.html')


class PledgeLoaderView:

    def pledges(self, request):
        if request.method == "POST":
            return self.__pledges_post_request(request)
        elif request.method == "GET":
            return self.__pledges_post_request(request)
        else:
            return HttpResponse("<h1>Error</h1>")

    def __pledges_post_request(self, request):

        # Parse post data and handle functions

        footprint, _ = CarbonFootprint.objects.get_or_create(business=test_business, year=2022)
        # Handle footprint error

        pledge_functions = PledgeFunctions(footprint)
        func_map = pledge_functions.get_func_map()

        data = request.POST

        # Parse post data into python dictionary
        data = dict(data)
        del data["csrfmiddlewaretoken"]

        pledge_functions_results = {key: func_map[key](value) for key, value in data.items()}

        # save pledge_functions_results to database
        #
        #

        # redirect to remove pledge page
        repsonse = redirect('/my/pledge_report')
        return repsonse


    def  __pledges_get_request(self, request):
        return render(request, 'calculator_site/pledges.html')

class CalculatorLoaderView:

    def __init__(self):
        file = open("static/JS/verbose.json")
        self.verbose = json.load(file)
        file.close()

        # TODO
        #  Should be called every request with login data
        test_business = Business.objects.get(company_name="test_business")
        self.footprint, _ = CarbonFootprint.objects.get_or_create(business=test_business, year=2022)

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

        # TODO
        #  Parse cookie data here to query database

        sh28 = User.objects.get(username="sh28")
        test_business = Business.objects.get(company_name="test_business")
        footprint, _ = CarbonFootprint.objects.get_or_create(business=test_business, year=2022)

        # Save data to database
        for k, v in data.items():
            setattr(footprint, k, v)
        footprint.save()

        # Updates current footprint
        # TODO
        #   Only update fields that are required, compare this to dictionary

        self.footprint = footprint
        return self.__calculator_get_request(request)

    def __calculator_get_request(self, request, progress=0):
        # Initialise data fields
        cal_form = CalculatorForm()
        proper_names = self.verbose["fields"]
        category_links = self.verbose["category_links"]
        category_names = self.verbose["categories"]
        conversion_factors = self.verbose["conversion_factors"]

        # Wrap specific fields in object
        fields = [CalculatorDataWrapper(key, cal_form[key], proper_names[key], conversion_factors[key])
                  for key in list(proper_names.keys())]

        # Sort fields into categories wrapping into objects
        category_list = []
        field_list = []
        for field in fields:
            link = category_links.get(field.id)
            field_list.append(field)
            if link is not None:
                category_list.append(CalculatorCategoryWrapper(link, category_names[link], field_list))
                field_list = []

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
            database_value = getattr(self.footprint, cal_data_wrapper.id)
            if database_value == -1:
                database_value = " "
            elif database_value == 0:
                cal_data_wrapper.checked = "unchecked"
            else:
                cal_data_wrapper.input_value = f"{database_value / cal_data_wrapper.conversion}"
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
