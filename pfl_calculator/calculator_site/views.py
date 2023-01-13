import json

from django.shortcuts import render
from calculator_site.forms import CalculatorForm
from calculator_site.models import BusinessUsage
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
    return render(request, 'calculator_site/scope.html')

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
    if  request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(username=username, password=password)
        return HttpResponse(request, 'login.html')

def about(request):
    if  request.method == 'GET':
        return render(request, 'register.html')
    else:
        return HttpResponse(request, 'about.html')




class CalculatorDataWrapper:

    def __init__(self):
        file = open("static/verbose.json")
        self.verbose = json.load(file)
        file.close()



    def calculator(self, request):
        cal_form = CalculatorForm()
        context = {}
        context['conversion_factor'] = "" #GET
        bu = BusinessUsage()
        fields = list(bu.__dict__.keys())
        del bu
        non_cal_fields = ['_state', 'id', 'business_id', 'conversion_factor_id', 'year']
        # List to preserve order
        calculator_fields = [field for field in fields if field not in non_cal_fields]
        # Tuple so that can index into cal_form field (maybe custom object better?)
        print(self.verbose)
        context["fields"] = [(field, cal_form[field]) for field in calculator_fields[:7]]
        return render(request, 'calculator_site/calculator.html', context=context)

