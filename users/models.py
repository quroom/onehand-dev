from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.permissions import IsAuthenticated
from ipware.ip import get_ip

class CustomUser(AbstractUser):
    pass

@receiver(user_logged_in, sender=CustomUser)
def post_login(sender, user, request, **kwargs):
    user.profile.ip_address = get_ip(request)
    user.profile.save()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, blank=True)
    birthday = models.DateField(null=True, blank=True)
    mobile_numer = PhoneNumberField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    signature = models.ImageField(blank=True)
    bank_name = models.CharField(max_length=45, blank=True)
    account_number = models.CharField(max_length=45, blank=True)
    point = models.IntegerField(default=0)
    category = models.IntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True)
    average_response_time = models.FloatField(default=0)
    response_rate = models.FloatField(default=0)
    contract_success_rate = models.FloatField(default=0)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if user.is_staff:
            Profile.objects.create(user=instance, category=1)
        else:
            Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
