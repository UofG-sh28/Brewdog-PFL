from django.shortcuts import render
from calculator_site.forms import CalculatorForm
from calculator_site.models import BusinessUsage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'calculator_site/index.html')

def outline(request):
    return render(request, 'calculator_site/outline.html')

def scope(request):
    return render(request, 'calculator_site/scope.html')

def calculator(request):
    cal_form = CalculatorForm(use_required_attribute=False)
    context = {}
    context['conversion_factor'] = "" #GET
    bu = BusinessUsage()
    fields = list(bu.__dict__.keys())
    del bu
    non_cal_fields = ['_state', 'id', 'business_id', 'conversion_factor_id', 'year']
    # List to preserve order
    calculator_fields = [field for field in fields if field not in non_cal_fields]
    # Tuple so that can index into cal_form field (maybe custom object better?)
    context["fields"] = [(field, cal_form[field]) for field in calculator_fields[:7]]
    return render(request, 'calculator_site/calculator.html', context=context)
