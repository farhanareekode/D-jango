from django.contrib.auth.models import User
from django.http import HttpResponseForbidden,HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
import razorpay




# Create your views here.
@login_required()
def payments(request, identifier):
    # Retrieve overview and user objects from the database
    user = get_object_or_404(CustomUser, username=identifier)
    # Retrieve the current user
    current_user = request.user
    # Check if the requested username matches the current user's username
    if identifier == current_user.username:
        pass
    else:
        return HttpResponseForbidden("Access Denied")
    client = razorpay.Client(auth=("rzp_test_HCvc3q3BZPRcGl", "qXUVJmb7GlPdcdR3JuwJlHnN"))
    data = {"amount": 500, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = client.order.create(data=data)
    order_id = payment['id']

    return render(request, 'payments/make_payment.html', {'order_id': order_id})
