from django import forms
from django.forms import TextInput
from calculator_site import models




class CalculatorUtil:

    @staticmethod
    def retrieve_meta_fields():
        bu = models.BusinessUsage()
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
            attrs = {'type': 'text', 'class': 'output', 'id': field + 'Output', 'placeholder': ' '}
            widgets[field] = TextInput(attrs=attrs)
        return widgets


class CalculatorForm(forms.ModelForm):



    class Meta:
        model = models.BusinessUsage
        fields = CalculatorUtil.retrieve_meta_fields()
        widgets = CalculatorUtil.retrieve_meta_widgets()

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)





