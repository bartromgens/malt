from django import forms

from glass.models import Glass

class NumberInput(forms.widgets.TextInput):
    input_type = 'number'

class NewDrinkForm(forms.ModelForm):
  emptiesBottle = forms.BooleanField(label='Bottle empty', required=False)
  
  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user')
    super(NewDrinkForm, self).__init__(*args, **kwargs)
    
    self.fields['user'].initial = user

  class Meta:
    model = Glass
    exclude = ('date','rating', 'mass')
    widgets = {'volume': NumberInput()}