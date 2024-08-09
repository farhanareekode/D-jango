from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from home.models import Booking
import razorpay

client = razorpay.Client(auth=("rzp_test_HCvc3q3BZPRcGl", "qXUVJmb7GlPdcdR3JuwJlHnN"))


@login_required()
def payments(request, identifier, booking_id):
    # Retrieve overview and user objects from the database
    user = get_object_or_404(CustomUser, username=identifier)
    booking_details = get_object_or_404(Booking, id=booking_id)

    # Retrieve the current user
    current_user = request.user
    # Check if the requested username matches the current user's username
    if identifier == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    data = {"amount": 500, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = client.order.create(data=data)
    order_id = payment['id']
    context = {
        'user': user,
        'order_id': order_id,
    }
    print(payment)
    return render(request, 'payments/make_payment.html', context)


@login_required()
def success(request, identifier):
    user = get_object_or_404(CustomUser, username=identifier)
    # Retrieve the current user
    current_user = request.user
    if identifier == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")

    return render(request, 'payments/success.html')
