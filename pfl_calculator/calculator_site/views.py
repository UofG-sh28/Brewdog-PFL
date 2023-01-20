import json

from django.shortcuts import render
from calculator_site.forms import CalculatorForm
from calculator_site.models import Business, CarbonFootprint
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth.models import User
from django.shortcuts import redirect


# INFO PAGES AND HOMEPAGE
def index(request):
    return render(request, 'calculator_site/index.html')


def outline(request):
    return render(request, 'calculator_site/outline.html')


def scope(request):
    data = Business.objects.all().values()
    context = {'business': data}
    return render(request, 'calculator_site/scope.html', context)


# AUTHENTICATED USER PAGES
def dash(request):
    return render(request, 'calculator_site/dashboard.html')


def metrics(request):
    return render(request, 'calculator_site/metrics.html')


def report(request):
    return render(request, 'calculator_site/report.html')


def pledges(request):
    return render(request, 'calculator_site/pledges.html')


def action_plan(request):
    return render(request, 'calculator_site/action_plan.html')


def profile(request):
    return render(request, 'calculator_site/profile.html')


def how_it_works(request):
    return render(request, 'calculator_site/how_it_works.html')

# LOGIN AND REGISTER PAGES
def login(request):
    if request.method == 'POST':
        username = request.post['username']
        password = request.post['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            lg(request, user)
            return HttpResponse(request, 'calculator_site/index.html')
        else:
            return HttpResponse(request, 'calculator_site/login.html')
    return render(request, 'calculator_site/login.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return HttpResponse(request, 'login.html')


def about(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        return HttpResponse(request, 'about.html')


class CalculatorLoaderView:

    def __init__(self):
        file = open("static/verbose.json")
        self.verbose = json.load(file)
        file.close()

        test_business = Business.objects.get(company_name="test_business")
        footprint = CarbonFootprint.objects.get(business=test_business, year=2022)
        self.footprint = footprint



    def calculator(self, request):
        if request.method == "POST":
            return self.__calculator_post_request(request)
        elif request.method == "GET":
            return self.__calculator_get_request(request)
        else:
            return HttpResponse("<h1>Error</h1>")

    def __calculator_post_request(self, request):
        data = request.POST


        data = dict(data)
        del data["csrfmiddlewaretoken"]
        data = {key: 0.0 if value[0] == "" or value[0] == " " else value[0] for key, value in data.items()}
        sh28 = User.objects.get(username="sh28")
        test_business = Business.objects.get(company_name="test_business")

        footprint, _ = CarbonFootprint.objects.get_or_create(business=test_business, year=2022)
        for k, v in data.items():
            setattr(footprint, k, v)
        footprint.save()

        self.footprint = footprint
        return self.__calculator_get_request(request)

    def __calculator_get_request(self, request, progress=0):
        cal_form = CalculatorForm()
        proper_names = self.verbose["fields"]
        category_links = self.verbose["category_links"]
        category_names = self.verbose["categories"]
        conversion_factors = self.verbose["conversion_factors"]
        fields = [CalculatorDataWrapper(key, cal_form[key], proper_names[key], conversion_factors[key])
                  for key in list(proper_names.keys())]

        category_list = []
        field_list = []
        for field in fields:
            link = category_links.get(field.id)
            field_list.append(field)
            if link is not None:
                category_list.append(CalculatorCategoryWrapper(link, category_names[link], field_list))
                field_list = []


        context = {}
        progress = int(request.GET.get('progress', progress))
        if progress > len(category_list)-1:
            repsonse = redirect('/my/report')
            return repsonse

        progress = max(0, progress)
        context["category"] = category_list[progress]

        for cal_data_wrapper in context["category"].fields:
            database_value = getattr(self.footprint, cal_data_wrapper.id)
            if database_value == 0.0:
                database_value = " "
            else:
                cal_data_wrapper.input_value = f"{database_value / cal_data_wrapper.conversion}"
            cal_data_wrapper.form.field.initial = database_value


        context["progress"] = progress+1
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
        self.input_value = ""
        self.checked = "checked"
