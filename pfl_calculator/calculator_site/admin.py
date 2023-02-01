from django.contrib import admin
from .models import  Business, BusinessMetrics, CarbonFootprint, Pledge, ActionPlan

# Register your models here.
admin.site.register(Business)
admin.site.register(BusinessMetrics)
admin.site.register(CarbonFootprint)
admin.site.register(Pledge)
admin.site.register(ActionPlan)
