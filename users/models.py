from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Ldap(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=200, default='')
    sAMAccountName = models.CharField(max_length=200, default='')
    objectSid = models.CharField(max_length=200, default='')
    userPrincipalName = models.CharField(max_length=200, default='')

