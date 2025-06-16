from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    name = models.CharField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Baby(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='babies', null=True, blank=True)
    name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    height_in = models.PositiveIntegerField(help_text='Height in inches', null=True, blank=True)
    weight_lb = models.FloatField(help_text='Weight in pounds', null=True, blank=True)
    photo = models.ImageField(upload_to='baby_photos/', null=True, blank=True)

    def __str__(self):
        return self.name


class Feeding(models.Model):
    BREAST_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
        ('both', 'Both'),
    ]
    
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=50, choices=[('bottle', 'Bottle'), ('breast', 'Breast'), ('solid', 'Solid')])
    amount_oz = models.PositiveIntegerField(null=True, blank=True)
    breast_used = models.CharField(max_length=5, choices=BREAST_CHOICES, blank=True, null=True)
    solid_food_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.baby.name} - {self.type} at {self.time.strftime('%Y-%m-%d %H:%M')}"


class Diaper(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=10, choices=[('wet', 'Wet'), ('dirty', 'Dirty'), ('both', 'Both')])

    def __str__(self):
        return f"{self.baby.name} - {self.type} diaper at {self.time.strftime('%Y-%m-%d %H:%M')}"


class Medicine(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dose_mg = models.FloatField(help_text='Dose in milligrams')
    time_given = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.baby.name} - {self.name} at {self.time_given.strftime('%Y-%m-%d %H:%M')}"


class Appointment(models.Model):
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    time = models.DateTimeField()
    reason = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def  __str__(self):
        return f"{self.baby.name} - Appointment with {self.doctor_name} on {self.time.strftime('%Y-%m-%d %H:%M')}"