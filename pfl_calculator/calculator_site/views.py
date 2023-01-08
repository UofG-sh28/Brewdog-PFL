from django.shortcuts import render
from calculator_site.forms import CalculatorForm
from calculator_site.models import BusinessUsage

# Create your views here.
def index(request):
    return render(request, 'calculator_site/index.html')

def outline(request):
    return render(request, 'calculator_site/outline.html')

def scope(request):
    return render(request, 'calculator_site/scope.html')

def calculator(request):
    context = {'cal_form': CalculatorForm()}
    context['conversion_factor'] = "" #GET
    bu = BusinessUsage()
    fields = list(bu.__dict__.keys())
    del bu
    non_cal_fields = ['_state', 'id', 'business_id', 'conversion_factor_id', 'year']
    # List to preserve order
    calculator_fields = [field for field in fields if field not in non_cal_fields]
    context["fields"] = calculator_fields[:7]
    return render(request, 'calculator_site/calculator.html', context=context)
