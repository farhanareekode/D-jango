from django.urls import path

from . import views

urlpatterns = [
    path('transaction/<str:identifier>/<int:booking_id>/', views.payments, name='payments'),
    path('success/<str:identifier>/<int:transactions_id>/', views.success, name='success')

]