from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput
from calculator_site import models

#Choices for business forms
AREA_TYPES = (
    ("C", "Inner City"),
    ("U", "Urban"),
    ("R", "Rural"),
)
PARTS_OF_WORLD = (
    ("UK", "UK"),
    ("EU","Europe"),
    ("NA","North America"),
    ("GL","Global"),
)
BUSINESS_TYPES = (
    ("BNFNA", "Bar (no food, no accomodation)"),
    ("BNA", "Bar (serving food, no accomodation)"),
    ("R", "Restaurant"),
    ("HNF", "Hotel (no food)"),
    ("H", "Hotel (serving Food)"),
)
BUSINESS_TURNOVERS = (
    ("S", "£100k-£500k"),
    ("M", "£500k-£10,000k"),
    ("L", "Over £10,000k"),
)
# Registration Form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class RegistrationFormStage2(forms.Form):
    """ Following a successful registration a user will be prompted to create their business """
    user = None
    company_name = forms.CharField(max_length=50)
    business_address = forms.CharField(max_length=150)
    area_type = forms.ChoiceField(choices=AREA_TYPES)
    part_of_world = forms.ChoiceField(choices=PARTS_OF_WORLD)
    business_type = forms.ChoiceField(choices=BUSINESS_TYPES)
    contact_number = forms.CharField(max_length=15)
    contact_email = forms.EmailField(max_length=150)
    business_size = forms.ChoiceField(choices=BUSINESS_TURNOVERS)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RegistrationFormStage2, self).__init__(*args, **kwargs)

    class Meta:
        fields = ("user", "company_name", "business_address", "area_type", "part_of_world", "business_type", "contact_number", "contact_email", "business_size")


    def save(self, commit=True):
        business = models.Business(user=self.user, company_name=self.cleaned_data['company_name'], business_address=self.cleaned_data['business_address'], area_type=self.cleaned_data['area_type'], part_of_world=self.cleaned_data['part_of_world'], business_type=self.cleaned_data['business_type'], contact_number=self.cleaned_data['contact_number'], contact_email=self.cleaned_data['contact_email'], business_size=self.cleaned_data['business_size'])
        business.save()



class CalculatorUtil:

    @staticmethod
    def retrieve_meta_fields():
        bu = models.CarbonFootprint()
        fields = list(bu.__dict__.keys())
        del bu
        non_cal_fields = ['_state', 'id', 'business_id', 'conversion_factor_id', 'year']
        # List to preserve order
        calculator_fields = [field for field in fields if field not in non_cal_fields]
        return tuple(calculator_fields)

    @staticmethod
    def retrieve_meta_widgets():
        fields = CalculatorUtil.retrieve_meta_fields()
        widgets = {}
        for field in fields:
            attrs = {'type': 'text', 'class': 'output input-style', 'id': field + 'Output', 'placeholder': ' ',
                     "value": " ", "required": "false"}
            widgets[field] = TextInput(attrs=attrs)
        return widgets


class CalculatorForm(forms.ModelForm):

    class Meta:
        model = models.CarbonFootprint
        fields = CalculatorUtil.retrieve_meta_fields()
        widgets = CalculatorUtil.retrieve_meta_widgets()

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ActionPlanUtil:

    @staticmethod
    def retrieve_meta_fields():
        bu = models.ActionPlan()
        fields = list(bu.__dict__.keys())
        del bu
        non_act_fields = ['_state', 'id', 'business_id', 'year']
        # List to preserve order
        action_plan_fields = [field for field in fields if field not in non_act_fields]
        return tuple(action_plan_fields)

    @staticmethod
    def retrieve_meta_widgets():
        fields = ActionPlanUtil.retrieve_meta_fields()
        widgets = {}
        for field in fields:
            attrs = {'type': 'text', 'class': 'pledge-input', 'id': field + '-pledge-input',
                     "value": ""}
            widgets[field] = TextInput(attrs=attrs)
        return widgets



class ActionPlanForm(forms.ModelForm):

    class Meta:
        model = models.ActionPlan
        fields = ActionPlanUtil.retrieve_meta_fields()
        widgets = ActionPlanUtil.retrieve_meta_widgets()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
