from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)




