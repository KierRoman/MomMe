from django import forms
from .models import Feeding, UserProfile, Medicine, Appointment


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'profile_pic']

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['type', 'breast_used', 'amount_oz', 'solid_food_name', 'time']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'dose_mg', 'time_given', 'notes']
        widgets = {
            'time_given': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor_name', 'location', 'latitude', 'longitude', 'time', 'reason', 'notes']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update({'id': 'id_location'})
        