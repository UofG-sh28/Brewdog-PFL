from django.http.response import JsonResponse
from calculator_site.models import Business, CarbonFootprint
from django.forms.models import model_to_dict




def get_footprint(request):
    if request.method == "GET":
        test_business = Business.objects.get(company_name="test_business")
        carbon = CarbonFootprint.objects.filter(business=test_business, year=2022).first()
        return JsonResponse(model_to_dict(carbon))

