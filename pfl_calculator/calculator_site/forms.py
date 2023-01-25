from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput
from calculator_site import models

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
                     "value": " "}
            widgets[field] = TextInput(attrs=attrs)
        return widgets


class CalculatorForm(forms.ModelForm):


    class Meta:
        model = models.CarbonFootprint
        fields = CalculatorUtil.retrieve_meta_fields()
        widgets = CalculatorUtil.retrieve_meta_widgets()

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
