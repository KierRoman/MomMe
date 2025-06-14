from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Baby, UserProfile, Feeding, Diaper, Medicine, Appointment
# Create your views here.

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

@login_required
def dashboard(request):
    babies = request.user.babies.all()

    for baby in babies:
        baby.latest_feeding = baby.feeding_set.order_by('-time').first()
        baby.latest_diaper = baby.diaper_set.order_by('-time').first()
        baby.current_medicine = baby.medicine_set.order_by('-time_given').first()
        baby.next_appointment = baby.appointment_set.filter(time__gte=timezone.now()).order_by('time').first()
    return render(request, 'dashboard.html', {'babies': babies})

def home(request):
    return render(request, 'home.html')


@login_required
def feedings(request):
    babies = request.user.babies.all()

    for baby in babies:
        baby.latest_feeding = baby.feeding_set.order_by('-time').first()

    return render(request, 'baby/feedings.html', {'babies': babies})

@login_required
def user_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'user/profile.html', {'profile': profile})

@login_required
def medicines(request):
    babies = request.user.babies.all()
    return render(request, 'baby/medicines.html', {'babies': babies})