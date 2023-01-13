import json

from django.shortcuts import render
from calculator_site.forms import CalculatorForm
from calculator_site.models import BusinessUsage, Business
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth.models import User


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


# LOGIN AND REGISTER PAGES
def login(request):
    if request.method == 'POST':
        username = request.post['username']
        password = request.post['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            lg(request, user)
            return HttpResponse(request, 'index.html')
        else:
            return HttpResponse(request, 'login.html')
    return render(request, 'login.html')


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

    def calculator(self, request):
        cal_form = CalculatorForm()
        proper_names = self.verbose["fields"]
        category_links = self.verbose["category_links"]
        category_names = self.verbose["categories"]
        fields = [CalculatorDataWrapper(key, cal_form[key], proper_names[key], 0.22)
                  for key in list(proper_names.keys())]

        category_list = []
        field_list = []
        for field in fields:
            link = category_links.get(field.id)
            if link is None:
                field_list.append(field)
            else:
                category_list.append(CalculatorCategoryWrapper(link, category_names[link], field_list))
                field_list = []

        context = {"categories": category_list}

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
