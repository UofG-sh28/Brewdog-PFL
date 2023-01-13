from django.contrib import admin
from .models import  Business, BusinessUsage, BusinessMetrics, ConversionFactor, CarbonFootprint

# Register your models here.
admin.site.register(Business)
admin.site.register(BusinessUsage)
admin.site.register(BusinessMetrics)
admin.site.register(ConversionFactor)
admin.site.register(CarbonFootprint)
