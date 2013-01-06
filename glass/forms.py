from django import forms

from glass.models import Glass

class NewDrinkForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user')
    super(NewDrinkForm, self).__init__(*args, **kwargs)
    
    self.fields['user'].initial = user

  class Meta:
    model = Glass
    exclude = ('date','rating', 'mass')