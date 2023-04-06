import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, Select, Textarea, DateInput
from calculator_site import models

# Choices for business forms
AREA_TYPES = (
    ("C", "Inner City"),
    ("U", "Urban"),
    ("R", "Rural"),
)
PARTS_OF_WORLD = (
    ("UK", "UK"),
    ("EU", "Europe"),
    ("NA", "North America"),
    ("GL", "Global"),
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
        fields = (
            "user", "company_name", "business_address", "area_type", "part_of_world", "business_type", "contact_number",
            "contact_email", "business_size")

    def save(self):
        business = models.Business(user=self.user, company_name=self.cleaned_data['company_name'],
                                   business_address=self.cleaned_data['business_address'],
                                   area_type=self.cleaned_data['area_type'],
                                   part_of_world=self.cleaned_data['part_of_world'],
                                   business_type=self.cleaned_data['business_type'],
                                   contact_number=self.cleaned_data['contact_number'],
                                   contact_email=self.cleaned_data['contact_email'],
                                   business_size=self.cleaned_data['business_size'])
        business.save()


class AdminUtil:

    @staticmethod
    def retrieve_meta_fields():
        bu = models.CarbonFootprint()
        fields = list(bu.__dict__.keys())
        del bu
        non_cal_fields = ['_state', 'id', 'business_id', 'conversion_factor_id', 'year']
        # List to preserve order
        calculator_fields = [field for field in fields if field not in non_cal_fields]
        return tuple(calculator_fields)


class AdminForm(forms.Form):
    class Meta:
        fields = AdminUtil.retrieve_meta_fields()

    year = forms.IntegerField()
    mains_gas = forms.DecimalField()
    fuel = forms.DecimalField()
    oil = forms.DecimalField()
    coal = forms.DecimalField()
    wood = forms.DecimalField()
    grid_electricity = forms.DecimalField()
    grid_electricity_LOWCARBON = forms.DecimalField()
    waste_food_landfill = forms.DecimalField()
    waste_food_compost = forms.DecimalField()
    waste_food_charity = forms.DecimalField()
    bottles_recycle = forms.DecimalField()
    aluminum_can_recycle = forms.DecimalField()
    general_waste_landfill = forms.DecimalField()
    general_waste_recycle = forms.DecimalField()
    special_waste = forms.DecimalField()
    goods_delivered_company_owned = forms.DecimalField()
    goods_delivered_contracted = forms.DecimalField()
    travel_company_business = forms.DecimalField()
    flights_domestic = forms.DecimalField()
    flights_international = forms.DecimalField()
    staff_commuting = forms.DecimalField()
    beef_lamb = forms.DecimalField()
    other_meat = forms.DecimalField()
    lobster_prawn = forms.DecimalField()
    fin_fish_seafood = forms.DecimalField()
    milk_yoghurt = forms.DecimalField()
    cheeses = forms.DecimalField()
    fruit_veg_local = forms.DecimalField()
    fruit_veg_other = forms.DecimalField()
    dried_food = forms.DecimalField()
    beer_kegs = forms.DecimalField()
    beer_cans = forms.DecimalField()
    beer_bottles = forms.DecimalField()
    beer_kegs_LOWCARBON = forms.DecimalField()
    beer_cans_LOWCARBON = forms.DecimalField()
    beer_bottles_LOWCARBON = forms.DecimalField()
    soft_drinks = forms.DecimalField()
    wine = forms.DecimalField()
    spirits = forms.DecimalField()
    kitchen_equipment_assets = forms.DecimalField()
    building_repair_maintenance = forms.DecimalField()
    cleaning = forms.DecimalField()
    IT_Marketing = forms.DecimalField()
    main_water = forms.DecimalField()
    sewage = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
            widgets[field] = Select(attrs=attrs)
        return widgets


class ActionPlanForm(forms.ModelForm):
    class Meta:
        model = models.ActionPlan
        fields = ActionPlanUtil.retrieve_meta_fields()
        widgets = ActionPlanUtil.retrieve_meta_widgets()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ChangePasswordForm(PasswordChangeForm):
    def clean_new_pass(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password and new_password_confirm and new_password != new_password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return new_password_confirm


class FeedbackUtil:

    @staticmethod
    def retrieve_meta_fields():
        fb = models.Feedback()
        fields = list(fb.__dict__.keys())
        del fb
        non_act_fields = ['_state', 'id', 'user_id']
        # List to preserve order
        feedback_fields = [field for field in fields if field not in non_act_fields]

        return tuple(feedback_fields)

    @staticmethod
    def retrieve_meta_widgets():
        fields = FeedbackUtil.retrieve_meta_fields()
        widgets = {}
        for field in fields:
            if re.match('^comment.', field):
                attrs = {'type': 'text', 'class': 'input-style', 'id': field + 'Input', 'placeholder': ' ',
                         "value": " ", "required": "false"}
                widgets[field] = TextInput(attrs=attrs)
            else:
                attrs = {'type': 'text', 'class': 'pledge-input', 'id': field + '-pledge-input',
                         "value": ""}
                widgets[field] = Select(attrs=attrs)

        return widgets


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = FeedbackUtil.retrieve_meta_fields()

        widgets = FeedbackUtil.retrieve_meta_widgets()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ActionPlanDetailUtil:

    @staticmethod
    def retrieve_meta_fields():
        fb = models.ActionPlanDetail()
        fields = list(fb.__dict__.keys())
        del fb
        non_act_fields = ['_state', 'id', 'business_id', 'year']
        # List to preserve order
        action_plan_detail_fields = [field for field in fields if field not in non_act_fields]

        return tuple(action_plan_detail_fields)

    @staticmethod
    def retrieve_meta_widgets():
        fields = ActionPlanDetailUtil.retrieve_meta_fields()
        widgets = {}
        for field in fields:
            if field == "ownership":
                attrs = {'type': 'text', 'class': 'action-plan-input-style', 'id': field + 'PlanInput', 'placeholder': ' ',
                         "value": " ", "required": "false"}
                widgets[field] = TextInput(attrs=attrs)
            elif field == "plan_detail":
                attrs = {'type': 'text', 'id': field + 'PlanTextarea', 'placeholder': ' ',
                         "value": " ", "required": "false"}
                widgets[field] = Textarea(attrs)
            elif field == "start_date":
                attrs_ = {'type': 'date'}
                widgets[field] = DateInput(attrs=attrs_)
            else:
                attrs = {'type': 'date'}
                widgets[field] = DateInput(attrs=attrs)

        return widgets


class ActionPlanDetailForm(forms.ModelForm):
    class Meta:
        model = models.ActionPlanDetail
        fields = ActionPlanDetailUtil.retrieve_meta_fields()
        widgets = ActionPlanDetailUtil.retrieve_meta_widgets()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
