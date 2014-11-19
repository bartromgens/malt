from django import forms
from userprofile.models import UserProfile

class EditUserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditUserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ('displayname',)
