from django.test import TestCase
from calculator_site.models import *

# Create your tests here.
class CreateBusiness(TestCase):
    user = User(username='test')

    business = Business(
        company_name = "TestBusiness",
        business_address = "Glasgow-ish",
        area_type = "U",
        part_of_world = "UK",
        business_type = "H",
        contact_number = "999",
        business_size = "M"
    )
