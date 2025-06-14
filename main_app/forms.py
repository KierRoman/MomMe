from django import forms
from .models import Feeding

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['time', 'type', 'amount_ml']
        widgets = {
            'time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }