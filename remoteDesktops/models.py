from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth import get_user_model

class BaseBoard(models.Model):
    bios_uuid = models.CharField(max_length=200, unique=True)
    sn = models.CharField(max_length=200, unique=True)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class MemoryType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class MachineInformation(models.Model):
    guid = models.CharField(max_length=200, unique=True)
    motherboard = models.ForeignKey(BaseBoard, on_delete=models.CASCADE)
    primary_owner_name = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    system_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class CpuInformation(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    processor_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    cores = models.IntegerField()
    max_clock_speed = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class GpuInformation(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pnp_device_id = models.CharField(max_length=200, unique=True)
    vertical_resolution = models.IntegerField()
    horizontal_resolution = models.IntegerField()
    max_refresh_rate = models.IntegerField()
    colors = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class MemoryInformation(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    type = models.ForeignKey(MemoryType, on_delete=models.CASCADE)
    capacity = models.CharField(max_length=100)
    speed = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    sn = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class MemoryStatistics(models.Model):
    memory = models.ForeignKey(MemoryInformation, on_delete=models.CASCADE)
    total_size = models.CharField(max_length=100)
    used_size = models.CharField(max_length=100)
    free_size = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class NetworkAdapter(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    mac_address = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class NetworkAdapterStatistics(models.Model):
    adapter = models.ForeignKey(NetworkAdapter, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    speed = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class DiskDrive(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sn = models.CharField(max_length=200, unique=True)
    size = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class VolumeInformation(models.Model):
    disk = models.ForeignKey(DiskDrive, on_delete=models.CASCADE)
    partition = models.CharField(max_length=200)
    volume_label = models.CharField(max_length=200)
    file_system = models.CharField(max_length=200)
    drive_letter = models.CharField(max_length=200)
    health = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    total_size = models.CharField(max_length=200)
    free_space = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class GeoLocation(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class GeoLocationLog(models.Model):
    geo_location = models.ForeignKey(GeoLocation, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class PnpDevice(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class AssignDesktopManager(models.Manager):

    @staticmethod
    def __get_motherboard(motherboard):
        try:
            return BaseBoard.objects.get(bios_uuid=motherboard['bios_uuid'], sn=motherboard['sn'])
        except ObjectDoesNotExist:
            return BaseBoard.objects.create(**motherboard)

    def __get_machine(self, machine, motherboard):
        try:
            return MachineInformation.objects.get(machine_guid=machine['guid'])
        except ObjectDoesNotExist:
            return MachineInformation.objects.create(motherboard=self.__get_motherboard(motherboard), **machine)

    @staticmethod
    def __get_cpu(machine, cpu):
        try:
            return CpuInformation.objects.get(processor_id=cpu['processor_id'])
        except ObjectDoesNotExist:
            return CpuInformation.objects.create(machine=machine, **cpu)

    def __save_cpu_usage(self, machine, cpu):
        try:
            cpu = self.__get_cpu(machine, cpu)
        except Exception as error:
            print(error)
        else:
            pass

    def record(self, data):
        machine = self.__get_machine(data['machine'], data['motherboard'])

        self.__save_cpu_usage(machine, data['cpu'])

class Desktop(models.Model):
    machine = models.ForeignKey(MachineInformation, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AssignDesktopManager()
