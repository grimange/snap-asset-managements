from django.db import models
from django.contrib.auth import get_user_model


class EquipmentBrand(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class EquipmentBrandModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    brand = models.ForeignKey(EquipmentBrand, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class ProcessorBrand(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class ProcessorModel(models.Model):
    brand = models.ForeignKey(ProcessorBrand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    base_frequency = models.CharField(max_length=100)
    cache = models.CharField(max_length=100)
    max_turbo_frequency = models.CharField(max_length=100)
    cores = models.IntegerField(max_length=10)
    threads = models.IntegerField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class DisplayLaptop(models.Model):
    type = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    resolution = models.CharField(max_length=100)
    aspect_ratio = models.CharField(max_length=100)
    features = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class MemoryLaptop(models.Model):
    configuration = models.CharField(max_length=100)
    max_capacity = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class KeyboardTouchPad(models.Model):
    type = models.CharField(max_length=100)
    key_travel = models.CharField(max_length=100)
    features = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class CameraLaptop(models.Model):
    resolution = models.CharField(max_length=100)
    features = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class NetworkCommunicationLaptop(models.Model):
    wifi = models.CharField(max_length=100)
    bluetooth = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class BatteryLaptop(models.Model):
    capacity = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    features = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)


class LaptopSpec(models.Model):
    brand = models.ForeignKey(EquipmentBrand, on_delete=models.CASCADE)
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    operating_system = models.CharField(max_length=100)
    processor = models.ForeignKey(ProcessorModel, on_delete=models.CASCADE)
    graphics = models.CharField(max_length=100)
    display = models.ForeignKey(DisplayLaptop, on_delete=models.CASCADE)
    memory = models.ForeignKey(MemoryLaptop, on_delete=models.CASCADE)
    storage = models.TextField(blank=False)
    io_ports = models.TextField(blank=False)
    expansion_slots = models.TextField(blank=False)
    keyboard_touch_pad = models.CharField(max_length=100)
    camera = models.ForeignKey(CameraLaptop, on_delete=models.CASCADE)
    audio = models.TextField(blank=False)
    network = models.ForeignKey(NetworkCommunicationLaptop, on_delete=models.CASCADE)
    battery = models.ForeignKey(BatteryLaptop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
