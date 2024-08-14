from django.http import HttpResponseForbidden, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from home.models import Booking, PatientProfile
import razorpay
from .models import Transactions

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

    return render(request, 'payments/success.html')
