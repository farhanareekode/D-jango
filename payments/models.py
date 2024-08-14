from django.db import models
from home.models import PatientProfile, Booking


class Transactions(models.Model):
    patient_profile = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='transactions',
                                        null=True, blank=True)
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='booking_id', null=True,
                                      blank=True)
    payment_username = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateField(auto_now=True)
    time_stamp = models.DateTimeField(auto_now_add=True)




