from django.urls import path
from . import api_endpoints

urlpatterns = [
    path('get-footprint/', api_endpoints.get_footprint, name='footprint'),
]
