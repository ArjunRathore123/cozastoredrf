from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import UserManager
from django.utils import timezone
# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    contact=models.CharField(max_length=10)
    address=models.CharField(max_length=225)
    city=models.CharField(max_length=100)
    type_choice=(('seller','Seller'),('buyer','Buyer'),('admin','Admin'))
    user_type=models.CharField(max_length=10,choices=type_choice)
    created_at=models.DateTimeField(default=timezone.now)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    object= UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email
