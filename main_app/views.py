from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import FeedingForm, UserProfileForm, MedicineForm, AppointmentForm, CustomUserCreationForm, BabyForm, DiaperForm
from .models import Baby, UserProfile, Feeding, Diaper, Medicine, Appointment
# Create your views here.

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()


def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile = user.userprofile
            profile.name = form.cleaned_data.get('name')
            profile.bio = form.cleaned_data.get('bio')
            profile.profile_pic = form.cleaned_data.get('profile_pic')
            profile.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def add_baby(request):
    if request.method == 'POST':
        form = BabyForm(request.POST)
        if form.is_valid():
            baby = form.save(commit=False)
            baby.user = request.user
            baby.save()
            return redirect('dashboard')
    else:
        form = BabyForm()
    return render(request, 'baby/baby_form.html', {'form': form})

@login_required
def user_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'user/profile.html', {'profile': profile})

@login_required
def update_user_profile(request):
    profile,_ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user/profile_edit.html', {'form': form})


@login_required
def dashboard(request):
    babies = request.user.babies.all()

    if not babies.exists():
        return redirect('add_baby')

    for baby in babies:
        baby.latest_feeding = baby.feeding_set.order_by('-time').first()
        baby.latest_diaper = baby.diaper_set.order_by('-time').first()
        baby.current_medicine = baby.medicine_set.order_by('-time_given').first()
        baby.next_appointment = baby.appointment_set.filter(time__gte=timezone.now()).order_by('time').first()
    return render(request, 'dashboard.html', {'babies': babies})


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


@login_required
@require_POST
def delete_feeding(request, feeding_id):
    feeding = get_object_or_404(Feeding, id=feeding_id, baby__user=request.user)
    baby_id = feeding.baby.id
    feeding.delete()
    messages.success(request, 'Feeding deleted.')
    return redirect('feedings', baby_id=baby_id)


@login_required
def medicines(request, baby_id=None):
    if baby_id:
        baby = get_object_or_404(Baby, id=baby_id, user=request.user)
        medicines = baby.medicine_set.order_by('-time_given')
        return render (request, 'baby/medicines.html', {'baby': baby, 'medicines': medicines})
    else:
        babies = request.user.babies.all()
        for baby in babies:
            baby.latest_medicine = baby.medicine_set.order_by('-time_given').first()
        return render(request, 'baby/medicines.html', {'babies': babies})

@login_required
def add_medicine(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, user=request.user)

    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.baby = baby
            medicine.save()
            return redirect('medicines', baby_id=baby.id)
    else:
        form = MedicineForm()

    return render(request, 'baby/medicine_form.html', {'form': form, 'baby': baby})


@login_required
def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, baby__user=request.user)
    baby = medicine.baby

    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicines', baby_id=baby.id)
    else:
        form = MedicineForm(instance=medicine)

    return render(request, 'baby/medicine_form.html', {'form': form, 'baby': baby})


@login_required
@require_POST
def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id, baby__user=request.user)
    baby_id = medicine.baby.id
    medicine.delete()
    messages.success(request, 'Medicine deleted.')
    return redirect('medicines', baby_id=baby_id)

@login_required
def appointments(request, baby_id=None):
    if baby_id:
        baby = get_object_or_404(Baby, id=baby_id, user=request.user)
        appointments = baby.appointment_set.order_by('-time')
        return render(request, 'baby/appointments.html', {'baby': baby, 'appointments': appointments})
    else:
        babies = request.user.babies.all()
        for baby in babies:
            baby.next_appointment = baby.appointment_set.order_by('-time').first()
    return render(request, 'baby/appointments.html', {'babies': babies})
        

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, baby__user=request.user)

    context = {
        'appointment': appointment,
        'latitude': appointment.latitude,
        'longitude': appointment.longitude,
    }

    return render(request, 'baby/appointment_detail.html', context)

@login_required
def add_appointment(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.baby = baby
            appointment.save()
            return redirect('appointments', baby_id=baby.id)
        else:
            print(form.errors)
    else:
        form = AppointmentForm()
    return render(request, 'baby/appointment_form.html', {'form': form, 'baby': baby})
    

@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, baby__user=request.user)
    baby = appointment.baby

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments', baby_id=baby.id)
    else:
            form = AppointmentForm(instance=appointment)
    return render(request, 'baby/appointment_form.html', {'form': form, 'baby': baby})
    

@login_required
@require_POST
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, baby__user=request.user)
    baby_id = appointment.baby.id
    appointment.delete()
    messages.success(request, 'Appointment deleted.')
    return redirect('appointments', baby_id=baby_id)

@login_required
def diapers(request, baby_id=None):
    if baby_id:
        baby = get_object_or_404(Baby, id=baby_id, user=request.user)
        diapers = baby.diaper_set.order_by('-time')
        return render(request, 'baby/diapers.html', {'baby': baby, 'diapers': diapers})
    else:
        babies = request.user.babies.all()
        for baby in babies:
            baby.latest_diaper = baby.diaper_set.order_by('-time').first()
        return render(request, 'baby/diapers.html', {'babies': babies})
    

@login_required
def add_diaper(request, baby_id):
    baby = get_object_or_404(Baby, id=baby_id, user=request.user)

    if request.method == 'POST':
        form = DiaperForm(request.POST)
        if form.is_valid():
            diaper = form.save(commit=False)
            diaper.baby = baby
            diaper.save()
            return redirect('diapers', baby_id=baby.id)
    else:
        form = DiaperForm()

    return render(request, 'baby/diaper_form.html', {'form': form, 'baby': baby})


def edit_diaper(request, diaper_id):
    diaper = get_object_or_404(Diaper, id=diaper_id, baby__user=request.user)
    baby = diaper.baby

    if request.method == 'POST':
        form = DiaperForm(request.POST, instance=diaper)
        if form.is_valid():
            form.save()
            return redirect('diapers', baby_id=baby.id)
    else:
        form = DiaperForm(instance=diaper)

    return render(request, 'baby/diaper_form.html', {'form': form, 'baby': baby})

@login_required
@require_POST
def delete_diaper(request, diaper_id):
    diaper = get_object_or_404(Diaper, id=diaper_id, baby__user=request.user)
    baby_id = diaper.baby.id
    diaper.delete()
    messages.success(request, 'Diaper entry deleted.')
    return redirect('diapers', baby_id=baby_id)