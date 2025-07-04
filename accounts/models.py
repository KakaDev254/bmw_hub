from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    """
    Extends Django's built-in AbstractUser.
    """
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = CloudinaryField('image')

    is_customer = models.BooleanField(default=True)  # future use: for customer vs admin vs seller etc.

    def __str__(self):
        return self.username

