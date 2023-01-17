from django.contrib import admin
from .models import  Business, BusinessMetrics, CarbonFootprint

# Register your models here.
admin.site.register(Business)
admin.site.register(BusinessMetrics)
admin.site.register(CarbonFootprint)
