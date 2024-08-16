from accounts.models import CustomUser
from django.db import models
from django.conf import settings


# Create your models here.
class PatientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to='users', default='')
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    BLOOD_GROUP = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_grp = models.CharField(max_length=10, choices=BLOOD_GROUP, default='B+')


class Departments(models.Model):
    dep_name = models.CharField(max_length=100)
    dep_description = models.TextField()

    def __str__(self):
        return self.dep_name


class Doctors(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=255)
    doc_spec = models.CharField(max_length=255)
    dep_name = models.ForeignKey(Departments, on_delete=models.CASCADE)
    doc_image = models.ImageField(upload_to='doctors')

    def __str__(self):
        return 'Dr ' + self.doc_name + ' - (' + self.doc_spec + ')'


class Booking(models.Model):
    patient_profile = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='booking', null=True,
                                        blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    patient_name = models.CharField(max_length=255)
    patient_phone = models.CharField(max_length=10)
    patient_email = models.EmailField()
    doctor_name = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    is_payment = models.BooleanField(default=False)

    # def __str__(self):
    #     return 'Dr ' + self.doctor_name + ' - (' + self.doc_spec + ')'


class DoctorsProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # other fields...
    def __str__(self):
        return f'{self.user}'
