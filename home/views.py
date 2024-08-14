from datetime import timezone
from django.contrib import messages

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .forms import PatientProfileForm, BookingForm
from .models import PatientProfile, Departments, Doctors, Booking, DoctorsProfile
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseNotFound, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser


def index(request):
    return render(request, 'home/home.html')


@login_required
def doctor_profile(request, identifier):
    user = get_object_or_404(CustomUser, username=identifier, is_doctor=True)
    current_user = request.user

    if not user.is_approved:
        return HttpResponseForbidden('Access Denied. Wait for approval.')

    if identifier != current_user.username:
        return HttpResponseForbidden('Access Denied')

    try:
        # Fetch the Doctors instance using the user field
        doctor_instance = Doctors.objects.get(user=user)
    except Doctors.DoesNotExist:
        return HttpResponseForbidden(
            'Doctor profile does not exist in hospital data \n Contact to hospital management.')

    # Handle booking approval
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        if booking.doctor_name != doctor_instance:
            return HttpResponseForbidden('Access Denied')

        booking.is_approved = True
        booking.save()
        return redirect('doctor_profile', identifier=request.user.username)

    # Filter bookings by the correct doctor instance
    bookings = Booking.objects.filter(doctor_name=doctor_instance)
    return render(request, 'home/doctor_profile.html', {'user': user, 'bookings': bookings})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_doctors_profile(sender, instance, created, **kwargs):
    if created and instance.is_doctor:
        DoctorsProfile.objects.create(user=instance)


@login_required
def patient_profile_add_details(request):
    user = request.user
    # Try to get the existing profile
    patient_profile_details, created = PatientProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = PatientProfileForm(request.POST, request.FILES, instance=patient_profile_details)
        if form.is_valid():
            patient_profile_details = form.save(commit=False)
            patient_profile_details.user = user  # Associate the profile with the logged-in user
            patient_profile_details.save()
            return redirect('patient_profile', identifier=user.username)  # Provide the identifier argument here
        else:
            print(form.errors)  # Print form errors if not valid
    else:
        form = PatientProfileForm(instance=patient_profile_details)

    profile_dict = {
        'form': form,
        'user': user,

    }
    return render(request, 'home/patient_profile_details.html', profile_dict)


@login_required
def patient_profile(request, identifier):
    user = get_object_or_404(CustomUser, username=identifier)
    patient_profile, created = PatientProfile.objects.get_or_create(user=user)
    current_user = request.user

    # Check if the current user is accessing their own profile
    if identifier != current_user.username:
        return HttpResponseForbidden('Access Denied')

    add_details = PatientProfile.objects.filter(user=user)
    add_details_exists = add_details.exists()  # Check if there are any details
    booking_details = Booking.objects.filter(patient_profile=patient_profile, is_approved=True)
    future_bookings = Booking.objects.filter(patient_profile=patient_profile, booking_date__gte=timezone.now().date())
    past_bookings = Booking.objects.filter(patient_profile=patient_profile, booking_date__lt=timezone.now().date())
    context = {
        'add_details': add_details,
        'add_details_exists': add_details_exists,
        'booking_details': booking_details,
        'future_bookings': future_bookings,
        'past_bookings': past_bookings,
        'user': user,
        'patient_profile': patient_profile,
    }
    return render(request, 'home/patient_profile.html', context)


def department(request):
    dict_dept = {
        'dept': Departments.objects.all()
    }
    return render(request, 'home/department.html', dict_dept)


def doctors(request):
    dict_docs = {
        'doctors': Doctors.objects.all()
    }
    return render(request, 'home/doctors.html', dict_docs)


@login_required
def booking(request, identifier):
    user = get_object_or_404(CustomUser, username=identifier)

    # Check if the logged-in user is the same as the user whose bookings are being accessed
    if request.user != user:
        return redirect('login')

    user_profile = get_object_or_404(PatientProfile, user=user)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_appointment = form.save(commit=False)
            booking_appointment.user = request.user  # Set the user manually
            booking_appointment.patient_profile = user_profile
            booking_appointment.save()
            return redirect('patient_profile', user.username)  # Redirect to profile page
        else:
            print(form.errors)  # Debugging line to print form errors
    else:
        form = BookingForm()

    context = {
        'form': form,
    }
    return render(request, 'home/booking.html', context)
