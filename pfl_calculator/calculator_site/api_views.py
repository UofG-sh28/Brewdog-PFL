from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http.response import JsonResponse
from calculator_site.models import Business, CarbonFootprint
from django.forms.models import model_to_dict






def test_page(request):
    return render(request, 'calculator_site/test.html')

def database_api(request):
    if request.method == "GET":
        test_business = Business.objects.get(company_name="test_business")
        # try:
        carbon = CarbonFootprint.objects.filter(business=test_business, year=2022).first()
        return JsonResponse(model_to_dict(carbon))
        # except Exception:
        #     # failed
        #     return JsonResponse({"status": "failed"})



