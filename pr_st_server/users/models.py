from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Users(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    address = models.CharField(max_length=500)
    consentReceiveNews = models.BooleanField(default=False)
    consentPersonalData = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["first_name", "last_name", "email", "address",
                       "consentReceiveNews", "consentPersonalData"]
    FIELDS_TO_UPDATE = ["first_name", "last_name", "username", "email", "address",
                        "consentReceiveNews", "consentPersonalData"]
