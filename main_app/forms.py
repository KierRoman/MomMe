from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Feeding, UserProfile, Medicine, Appointment, Baby, Diaper


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'profile_pic']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BabyForm(forms.ModelForm):
    class Meta:
        model = Baby
        fields = ['name', 'birth_date']  # Add other fields if your Baby model has more
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

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

class DiaperForm(forms.ModelForm):
    class Meta:
        model = Diaper
        fields = ['time', 'type']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
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
        