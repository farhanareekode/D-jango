import statistics
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='home'),
    path('doctor/<str:username>/', views.doctor_profile, name='doctor_profile'),
    path('patient/<str:username>/', views.patient_profile, name='patient_profile'),

]
