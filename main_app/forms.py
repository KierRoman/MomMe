from django import forms
from .models import Feeding, UserProfile, Medicine, Appointment


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'profile_pic']

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['time', 'type', 'amount_ml']
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
        fields = ['doctor_name', 'location', 'time', 'reason', 'notes']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }