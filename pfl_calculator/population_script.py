import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pfl_calculator.settings')

import django
django.setup()
from calculator_site.models import *
from django.contrib.auth.models import User

def add_pledge(cat, text):
    p = Pledge.objects.get_or_create(category=cat, text=text)[0]
    p.save()
    return p

pledges = [
    {"category": "E","text": "Reduce electricity consumption"},
    {"category": "E","text": "Switch to a high quality 100% renewable electricity supplier (that matches all supply to all customers with 100% renewable power purchase agreements (PPAs).)"},
    {"category": "E","text": "Reduce gas consumption"},
    {"category": "E","text": "Reduce oil consumption"},
    {"category": "E","text": "Reduce coal consumption"},
    {"category": "E","text": "Reduce wood consumption"},
    {"category": "E","text": "Commission an energy augit undertaken with detailed energy advice"},
    {"category": "F","text": "Swap beef and lamb for non-animal alternatives"},
    {"category": "F","text": "Swap beef and lamb for other meat products"},
    {"category": "F","text": "Swap other meats for non-animal alternatives"},
    {"category": "F","text": "Replace high carbon fruit and veg (air freight, hot house) for low carbon fruit and veg (local, seasonal)"},
    {"category": "F","text": "Use a detailed menu carbon calculator to understand and reduce our food carbon"},
    {"category": "F","text": "Reduce food waste"},
    {"category": "F","text": "Carry out a waste audit"},
    {"category": "B","text": "Switch higher carbon beers to lower carbon beers"},
    {"category": "B","text": "Switch bottled beer to beer from reusable kegs"},
    {"category": "B","text": "Switch bottled beer to canned beer"},
    {"category": "B","text": "Switch our canned beer to beer from reusable kegs"},
    {"category": "W","text": "Reduce general waste"},
    {"category": "T","text": "Reduce vehicle road miles (company travel and deliveries)"},
    {"category": "T","text": "Reduce commuting vehicle road miles"},
    {"category": "T","text": "Reduce staff flights"},
    {"category": "O","text": "Reduce Emissions from Operations and Maintenance"},
    {"category": "M","text": "Adopt sustainable purchasing of non-food disposable items"},
    {"category": "M","text": "Sustainable procurement of equipment and furniture: where possible, buy pre-loved, sustainably produced or repair what we already have."},
]

def populate():
    for pledge in pledges[::-1]:
        add_pledge(pledge["category"], pledge["text"])


if __name__ == "__main__":
    print("Populating Pledges... ")
    populate()
    #     print("Successfully Populated...")
    # except:
    #     print("something went wrong...")
