from django.urls import path

from . import views

urlpatterns = [
    path('<str:identifier>/', views.payments, name='payments'),
    
]