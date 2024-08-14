
from datetime import datetime
from django import forms
from django.forms import DateInput

from .models import PatientProfile, Booking


class DateInput(forms.DateInput):
    input_type = 'date'


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['name', 'phone', 'image', 'address', 'country', 'state', 'blood_grp']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image'].label = 'Profile Photo'


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'booking_date': forms.DateInput(attrs={
                'type': 'date',
                'min': datetime.now().date().strftime('%Y-%m-%d')  # Set min to today
            })
        }
