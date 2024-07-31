from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from accounts.models import CustomUser
from .forms import PatientProfileForm
from .models import PatientProfile, Departments, Doctors


def index(request):
    return render(request, 'home/home.html')


@login_required
def doctor_profile(request, username):
    # Fetch user based on the username
    user = get_object_or_404(CustomUser, username=username, is_doctor=True)

    # Check if the doctor is approved
    if not user.is_approved:
        return HttpResponseForbidden('Access Denied. Waite for approved.')

    # Check if the current user is accessing their own profile
    if username == request.user.username:
        # Render the profile page for the current user
        return render(request, 'home/doctor_profile.html', {'user': user})
    else:
        return HttpResponseForbidden('Access Denied')


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
    current_user = request.user

    # Check if the current user is accessing their own profile
    if identifier != current_user.username:
        return HttpResponseForbidden('Access Denied')

    add_details = PatientProfile.objects.filter(user=user)
    add_details_exists = add_details.exists()  # Check if there are any details

    context = {
        'add_details': add_details,
        'add_details_exists': add_details_exists,
        'user': user,
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
