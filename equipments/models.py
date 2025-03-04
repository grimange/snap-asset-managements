from django.db import models
from django.contrib.auth import get_user_model

class EquipmentType(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class EquipmentBrand(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class EquipmentBrandModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    brand = models.ForeignKey(EquipmentBrand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class Equipment(models.Model):
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=150)
    notes = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
