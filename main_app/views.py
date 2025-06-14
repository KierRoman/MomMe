from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import FeedingForm
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
def feedings(request, baby_id=None):
    if baby_id:
        baby = get_object_or_404(Baby, id=baby_id, user=request.user)
        feedings = baby.feeding_set.order_by('-time')
        return render(request, 'baby/feedings.html', {'baby': baby, 'feedings': feedings})
    else:
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


@login_required
def add_feeding(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, user=request.user)

    if request.method == 'POST':
        form = FeedingForm(request.POST)
        if form.is_valid():
            feeding = form.save(commit=False)
            feeding.baby = baby
            feeding.save()
            return redirect('feedings', baby_id=baby.id)
    else:
        form = FeedingForm()

    return render(request, 'baby/feeding_form.html', {'form': form, 'baby': baby})

@login_required
def edit_feeding(request, feeding_id):
    feeding = get_object_or_404(Feeding, id=feeding_id, baby__user=request.user)

    if request.method == 'POST':
        form = FeedingForm(request.POST, instance=feeding)
        if form.is_valid():
            form.save()
            return redirect('feedings', baby_id=feeding.baby.id)
    else:
        form = FeedingForm(instance=feeding)

    return render(request, 'baby/feeding_form.html', {'form': form, 'baby': feeding.baby})