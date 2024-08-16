from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from home.models import Booking, PatientProfile
import razorpay
from .models import Transactions

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

client = razorpay.Client(auth=("rzp_test_HCvc3q3BZPRcGl", "qXUVJmb7GlPdcdR3JuwJlHnN"))


@login_required()
def payments(request, identifier, booking_id):
    # Retrieve overview and user objects from the database
    user = get_object_or_404(CustomUser, username=identifier)

    # Retrieve the current user
    current_user = request.user
    # Check if the requested username matches the current user's username
    if identifier == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    appointment_fee = 500
    online_payment_charge = 50
    total = appointment_fee + online_payment_charge

    data = {"amount": total * 100, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = client.order.create(data=data)
    order_id = payment['id']

    booking_details = get_object_or_404(Booking, id=booking_id)
    print(booking_details.id)  # This is fine for debugging

    transactions = Transactions.objects.create(
        payment_id=payment['id'],
        amount=total,
        booking_id=booking_details,  # Pass the Booking instance, not the ID
    )

    print(payment['id'])
    context = {
        'user': user,
        'order_id': order_id,
        'transactions': transactions,
    }
    return render(request, 'payments/make_payment.html', context)


@login_required
def success(request, identifier, transactions_id):
    user = get_object_or_404(CustomUser, username=identifier)
    current_user = request.user

    if identifier != current_user.username:
        return HttpResponseForbidden("Access Denied")

    transactions = get_object_or_404(Transactions, id=transactions_id)
    patient_profile = get_object_or_404(PatientProfile, user=current_user)

    # Access the booking using the booking_id field
    booking = transactions.booking_id
    payment_username = patient_profile.name
    if not booking:
        print("No booking found for this transaction.")
        return HttpResponseNotFound("No booking found.")

    print(f"Booking: {booking}")

    transactions.payment_status = True
    transactions.payment_username = payment_username
    transactions.save()

    booking.is_payment = True
    booking.save()

    user_details = get_object_or_404(PatientProfile, user=current_user)
    booking_details = get_object_or_404(Booking, id=booking.id, user=current_user)
    context = {
        'user_details': user_details,
        'transactions': transactions,
        'booking_details': booking_details,

    }

    return render(request, 'payments/success.html',context)


# def payment_pdf_view(request, identifier, booking_id):
#     current_user = request.user
#     if identifier != current_user.username:
#         return HttpResponseForbidden('Access Denied')
#     user_details = get_object_or_404(PatientProfile, user=current_user)
#     transactions = get_object_or_404(Transactions, patient_profile=user_details.user.id)
#     booking_details = get_object_or_404(Booking, id=booking_id, user=current_user)
#     template_path = 'payments/payment_report.html'
#
#     context = {
#         'user_details': user_details,
#         'transactions': transactions,
#         'booking_details': booking_details,
#
#         }
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     # to download
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#
#     # to view
#     response['Content-Disposition'] = 'filename="report.pdf"'
#
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#
#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

def payment_pdf_view(request, identifier, booking_id, action):
    current_user = request.user
    if identifier != current_user.username:
        return HttpResponseForbidden('Access Denied')

    user_details = get_object_or_404(PatientProfile, user=current_user)
    transactions = get_object_or_404(Transactions, patient_profile=user_details.user.id)
    booking_details = get_object_or_404(Booking, id=booking_id, user=current_user)

    template_path = 'payments/payment_report.html'
    context = {
        'user_details': user_details,
        'transactions': transactions,
        'booking_details': booking_details,
    }

    # Create a Django response object and specify content_type as PDF
    response = HttpResponse(content_type='application/pdf')

    # Set the Content-Disposition header based on the action parameter
    if action == 'download':
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    else:  # for view
        response['Content-Disposition'] = 'inline; filename="report.pdf"'

    # Find the template and render it
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # If error, return error message
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response
