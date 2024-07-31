from django import forms

from .models import PatientProfile


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['name', 'phone', 'image', 'address', 'country', 'state', 'blood_grp']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image'].label = 'Profile Photo'
