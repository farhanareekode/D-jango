from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request):
    return render(request, 'home/home.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from accounts.models import CustomUser # Make sure to import CustomUser

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
def patient_profile(request, username):
    # Fetch user based on the username
    user = get_object_or_404(CustomUser, username=username)

    # Check if the current user is accessing their own profile
    if username == request.user.username:
        # Render the profile page for the current user
        return render(request, 'home/patient_profile.html', {'user': user})
    else:
        return HttpResponseForbidden('Access Denied')
