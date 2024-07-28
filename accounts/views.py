from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import PatientRegistrationForm, DoctorRegistrationForm, LoginForm

def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home after registration
    else:
        form = PatientRegistrationForm()
    return render(request, 'accounts/register_patient.html', {'form': form})

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_doctor = True
            user.save()
            login(request, user)
            return redirect('home')  # Redirect to home after registration
    else:
        form = DoctorRegistrationForm()
    return render(request, 'accounts/register_doctor.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Debugging: Print user details and role
            print(f"Logged in user: {user.username}, is_doctor: {user.is_doctor}")

            # Check user role and redirect to their profile
            if user.is_doctor:
                return redirect('doctor_profile', username=user.username)
            else:
                return redirect('patient_profile', username=user.username)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

