from django.urls import path
from .views import payment_pdf_view
from . import views

urlpatterns = [
    path('transaction/<str:identifier>/<int:booking_id>/', views.payments, name='payments'),
    path('success/<str:identifier>/<int:transactions_id>/', views.success, name='success'),
    # path('payment_pdf_view/<str:identifier>/<int:booking_id>/', views.payment_pdf_view, name='payment_pdf_view')
    path('payment_pdf/download/<str:identifier>/<int:booking_id>/',
         payment_pdf_view, {'action': 'download'},
         name='payment_pdf_download'),

    # URL for viewing the PDF
    path('payment_pdf/view/<str:identifier>/<int:booking_id>/',
         payment_pdf_view, {'action': 'view'},
         name='payment_pdf_view'),

]
