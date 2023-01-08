from django.shortcuts import render
from calculator_site.forms import CalculatorForm

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

    return render(request, 'calculator_site/calculator.html', context=context)
