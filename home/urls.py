from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('doctor/<str:identifier>/', views.doctor_profile, name='doctor_profile'),
    path('patient/<str:identifier>/', views.patient_profile, name='patient_profile'),
    path('patient_profile_add_details', views.patient_profile_add_details, name='patient_profile_add_details'),
    path('department', views.department, name='department'),
    path('doctors', views.doctors, name='doctors'),
    path('booking/<str:identifier>', views.booking, name='booking'),
    path('doctor/profile/<str:identifier>/', views.doctor_profile, name='doctor_profile'),
]


