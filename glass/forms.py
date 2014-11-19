from django import forms

from glass.models import Glass

import logging

class NumberInput(forms.widgets.TextInput):
    input_type = 'number'

class NewDrinkForm(forms.ModelForm):
    emptiesBottle = forms.BooleanField(label='Bottle empty', required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        bottleId = 0
        if 'bottleId' in kwargs:
            bottleId = kwargs.pop('bottleId')

        super(NewDrinkForm, self).__init__(*args, **kwargs)

        self.fields['user'].initial = user

        if bottleId:
            self.fields['bottle'].initial = bottleId

    class Meta:
        model = Glass
        exclude = ('date','rating', 'mass')
        widgets = {'volume': NumberInput()}
