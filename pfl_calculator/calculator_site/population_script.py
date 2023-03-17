from .models import *
from django.contrib.auth.models import User

class PledgeSaver:
    def __init__(self, pledge_functions_results):
        self.pledge_functions_results = pledge_functions_results

    def save_pledge(self):
        # save Category and text
        count = 0
        for (key, value) in self.pledge_functions_results:
            pledges = Pledge()
            count += 1
            if count <= 7:
                pledges.category = 'E'
            elif count <= 14:
                pledges.category = 'F'
            elif count <= 18:
                pledges.category = 'B'
            elif count <= 19:
                pledges.category = 'W'
            elif count <= 22:
                pledges.category = 'T'
            elif count <= 23:
                pledges.category = 'O'
            else:
                pledges.category = 'M'
            pledges.text = key
            pledges.save()