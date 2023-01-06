from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'calculator_site/index.html')

def outline(request):
    return render(request, 'calculator_site/outline.html')

def scope(request):
    return render(request, 'calculator_site/scope.html')


def calculate(request):
    return render(request, 'calculator_site/calculator.html')