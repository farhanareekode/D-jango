from django.http import HttpResponseNotAllowed
from django.contrib.auth import login, logout
from .forms import PatientRegistrationForm, DoctorRegistrationForm, LoginForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import PatientRegistrationForm
from .models import CustomUser
import logging
logger = logging.getLogger(__name__)


def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            subject = 'Welcome to Life Care Hospital'
            message = (f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <h2 style="color: #2c3e50;">Dear {user.username},</h2>
                    <p><b>Thank you for registering at Life Care Hospital.</b></p>
                    <p>Your account has been created successfully. We are committed to 
                    providing you with the best healthcare services.</p>
                </body>
            </html>
            """)
            recipient = form.cleaned_data.get('email')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False,
                      html_message=message)
            messages.success(request, 'Success!')
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
            subject = 'Welcome to Life Care Hospital'
            message = (f"""
                        <html>
                            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                                <h2 style="color: #2c3e50;">Dear {user.username},</h2>
                                <p><b>Thank you for registering at Life Care Hospital.</b></p>
                                <p>Your account has been created successfully. We are committed to 
                                providing you with the best healthcare services.</p>
                                <p>Please login after only get your registration is approved mail</p> 
                            </body>
                        </html>
                        """)
            recipient = form.cleaned_data.get('email')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False,
                      html_message=message)
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

            # Check a user role and redirect to their profile
            if user.is_doctor:
                return redirect('doctor_profile', identifier=user.username)
            else:
                return redirect('patient_profile', identifier=user.username)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     return render(request, 'home/home.html')

def custom_logout_view(request):
    if request.method == 'POST' or request.method == 'GET':  # Allow both GET and POST
        logout(request)
        return redirect('home')  # Redirect to the homepage after logout
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
