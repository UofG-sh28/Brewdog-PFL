from django import forms
from django.forms import TextInput
from calculator_site import models

class CalculatorForm(forms.ModelForm):

    class Meta:
        model = models.BusinessUsage
        # Update to not be hard coded? static method?
        fields = ('mains_gas', 'fuel', 'oil', 'coal', 'wood', 'grid_electricity', 'grid_electricity_LOWCARBON')
        widgets = {
            'mains_gas': TextInput(attrs={
                'type': 'text',
                'class': 'output',
                'id': 'mains_gasOutput',
                'placeholder': ' '}),
            'fuel' : TextInput(attrs={
                'type': 'text',
                'class': 'output',
                'id': 'fuelOutput',
                'placeholder': ' '}),
            'oil': TextInput(attrs={
                'type': 'text',
                'class': 'output',
                'id': 'oilOutput',
                'placeholder': ' '}),
            'coal' : TextInput(attrs={
                'type': 'text',
                'class': 'output',
                'id': 'coalOutput',
                'placeholder': ' '}),
            'wood': TextInput(attrs={
                'type': 'text',
                'class': 'output',
                'id': 'woodOutput',
                'placeholder': ' '}),
            'grid_electricity' : TextInput(attrs={
                'type': 'text',
                'class': 'output',
                'id': 'grid_electricityOutput',
                'placeholder': ' '}),
            'grid_electricity_LOWCARBON' : TextInput(attrs={
                'type': 'text',
                'class': 'output',
                'id': 'grid_electricity_LOWCARBONOutput',
                'placeholder': ' '}),
        }
