import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

class BaseBoard(models.Model):
    bios_uuid = models.CharField(max_length=200, unique=True)
    sn = models.CharField(max_length=200, unique=True)
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class MachineInformation(models.Model):
    guid = models.CharField(max_length=200, unique=True)
    system_type = models.CharField(max_length=100)
    motherboard = models.ForeignKey(BaseBoard, on_delete=models.CASCADE)
    primary_owner_name = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    os_name = models.CharField(max_length=100, null=True)
    os_version = models.CharField(max_length=100, null=True)
    os_build = models.CharField(max_length=100, null=True)
    os_install_date = models.DateTimeField(null=True)
    last_boot_up = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CpuInformation(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    processor_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    cores = models.IntegerField()
    max_clock_speed = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class GpuInformation(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pnp_device_id = models.CharField(max_length=200, unique=True)
    vertical_resolution = models.IntegerField()
    horizontal_resolution = models.IntegerField()
    max_refresh_rate = models.IntegerField()
    colors = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class MemoryInformation(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    sn = models.CharField(max_length=200)
    part_number = models.CharField(max_length=100, null=True)
    device_locator = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100)
    speed = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class MemoryStatistics(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    total_size = models.BigIntegerField()
    used_size = models.BigIntegerField()
    free_size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class NetworkAdapter(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    mac_address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class NetworkLog(models.Model):
    adapter = models.ForeignKey(NetworkAdapter, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    speed = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class DiskDrive(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sn = models.CharField(max_length=200)
    size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class VolumeInformation(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    file_system = models.CharField(max_length=200)
    drive_letter = models.CharField(max_length=200, null=True)
    health_status = models.CharField(max_length=200)
    operational_status = models.CharField(max_length=200)
    size_remaining = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class GeoLocationLog(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=100, null=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class PnpDevice(models.Model):
    machine = models.ForeignKey(MachineInformation, null=True, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class CpuUsageLog(models.Model):
    cpu = models.ForeignKey(CpuInformation, on_delete=models.CASCADE)
    usage = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class AssignDesktopManager(models.Manager):

    @staticmethod
    def __get_motherboard(motherboard):
        try:
            return BaseBoard.objects.get(bios_uuid=motherboard['bios_uuid'], sn=motherboard['sn'])
        except ObjectDoesNotExist:
            return BaseBoard.objects.create(**motherboard)

    def __get_machine(self, machine, motherboard):
        try:
            machine2 = MachineInformation.objects.get(guid=machine['guid'])
            lbpObject = datetime.fromisoformat(machine['last_boot_up'])
            if machine2.last_boot_up != lbpObject:
                machine2.last_boot_up = lbpObject
                machine2.save()
            return machine2
        except ObjectDoesNotExist:
            return MachineInformation.objects.create(motherboard=self.__get_motherboard(motherboard), **machine)

    @staticmethod
    def __get_cpu(machine, cpu):
        try:
            return CpuInformation.objects.get(processor_id=cpu['processor_id'], machine=machine)
        except ObjectDoesNotExist:
            return CpuInformation.objects.create(machine=machine, **cpu)

    @staticmethod
    def __save_disk(machine, disk):
        try:
            return DiskDrive.objects.get(sn=disk['sn'], machine=machine)
        except ObjectDoesNotExist:
            return DiskDrive.objects.create(machine=machine, **disk)

    @staticmethod
    def __get_network_adapter(machine, network):
        try:
            return NetworkAdapter.objects.get(mac_address=network['mac_address'], machine=machine)
        except ObjectDoesNotExist:
            return NetworkAdapter.objects.create(machine=machine, name=network['name'],
                                                 description=network['description'], mac_address=network['mac_address'])

    @staticmethod
    def __save_volumes(machine, volumes):
        for volume in volumes:
            VolumeInformation.objects.create(machine=machine, **volume)

    def __save_disks(self, machine, disks):
        if type(disks) is list:
            for disk in disks:
                self.__save_disk(machine, disk)
        else:
            self.__save_disk(machine, disks)

    def __save_networks(self, machine, networks):
        for network in networks:
            adapter = self.__get_network_adapter(machine, network)
            self.__save_network(adapter, network)

    @staticmethod
    def __save_network(adapter, network):
        try:
            return NetworkLog.objects.get(adapter=adapter, ip_address=network['ip_address'])
        except ObjectDoesNotExist:
            return NetworkLog.objects.create(adapter=adapter, status=network['status'], speed=network['speed'],
                                             ip_address=network['ip_address'])

    def __save_rams(self, machine, rams):
        for ram in rams:
            self.__save_ram(machine, ram)

    @staticmethod
    def __save_ram(machine, memory):
        try:
            return MemoryInformation.objects.get(sn=memory['sn'], machine=machine)
        except ObjectDoesNotExist:
            return MemoryInformation.objects.create(machine=machine, **memory)

    @staticmethod
    def __save_gpu(machine, gpu):
        try:
            return GpuInformation.objects.get(pnp_device_id=gpu['pnp_device_id'], machine=machine)
        except ObjectDoesNotExist:
            return GpuInformation.objects.create(machine=machine, **gpu)

    def __save_pnp_devices(self, machine, pnp_devices):
        for pnp_device in pnp_devices:
            self.__save_pnp_device(machine, pnp_device)

    @staticmethod
    def __save_pnp_device(machine, pnp_device):
        try:
            return PnpDevice.objects.get(device_id=pnp_device['device_id'], machine=machine)
        except ObjectDoesNotExist:
            return PnpDevice.objects.create(machine=machine, **pnp_device)

    def __save_cpu_usage(self, machine, cpu):
        try:
            cpuObject = self.__get_cpu(machine, cpu)
        except Exception as error:
            print(error)
        else:
            CpuUsageLog.objects.create(cpu=cpuObject, usage=cpu['usage'])

    @staticmethod
    def __save_memory_usage(machine, memory_usage):
        MemoryStatistics.objects.create(machine=machine, **memory_usage)

    @staticmethod
    def __save_geo_location(machine, geo_location):
        if not GeoLocationLog.objects.filter(machine=machine, latitude=geo_location['latitude'], longitude=geo_location['longitude']).exists():
            GeoLocationLog.objects.create(machine=machine, **geo_location)

    def record_machine(self, data):
        machine = self.__get_machine(data['machine'], data['motherboard'])

        self.__save_cpu_usage(machine, data['cpu'])
        self.__save_gpu(machine, data['gpu'])
        self.__save_memory_usage(machine, data['memory_usage'])
        self.__save_geo_location(machine, data['geo_location'])
        self.__save_rams(machine, data['memory'])
        self.__save_pnp_devices(machine, data['pnp_devices'])
        self.__save_networks(machine, data['networks'])
        self.__save_disks(machine, data['disks'])
        self.__save_volumes(machine, data['volumes'])

class Desktop(models.Model):
    machine = models.ForeignKey(MachineInformation, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AssignDesktopManager()

class DesktopGlobalManager(models.Manager):
    @staticmethod
    def __get_machine(guid):
        return MachineInformation.objects.get(guid=guid)

    @staticmethod
    def __get_user(username):
        try:
            return get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            return get_user_model().objects.create(username=username)

    def __desktop(self, user, machine):
        try:
            user2 = self.__get_user(user)
            machine2 = self.__get_machine(machine)
            return Desktop.objects.get(user=user2, machine=machine2)
        except ObjectDoesNotExist:
            return Desktop.objects.create(user=user2, machine=machine2)

class ChromeUrlHistoryManager(DesktopGlobalManager):
    def __save_url(self, desktop, history):
        try:
            self.get(url=history['url'], desktop=desktop)
        except ObjectDoesNotExist:
            self.create(desktop=desktop, **history)

    def record(self, user, machine, urlHistories):
        desktop = self.__desktop(user, machine)
        for urlHistory in urlHistories:
            self.__save_url(desktop, urlHistory)

class ChromeUrlHistory(models.Model):
    desktop = models.ForeignKey(Desktop, null=True, on_delete=models.CASCADE)
    url = models.TextField()
    title = models.CharField(max_length=200)
    visit_count = models.IntegerField()
    type_count = models.IntegerField()
    last_visit_time = models.DateTimeField()
    hidden = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ChromeUrlHistoryManager()


class ChromeDownloadLogManager(DesktopGlobalManager):
    def __save_download(self, desktop, download):
        try:
            self.get(guid=download['guid'], desktop=desktop)
        except ObjectDoesNotExist:
            self.create(desktop=desktop, **download)

    def record(self, user, machine, downloads):
        desktop = self.__desktop(user, machine)
        for download in downloads:
            self.__save_download(desktop, download)

class ChromeDownloadLog(models.Model):
    desktop = models.ForeignKey(Desktop, null=True, on_delete=models.CASCADE)
    guid = models.CharField(max_length=200)
    target_path = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    received_bytes = models.BigIntegerField()
    total_bytes = models.BigIntegerField()
    state = models.IntegerField()
    danger_type = models.IntegerField()
    interrupt_reason = models.IntegerField()
    opened = models.IntegerField()
    last_access_time = models.DateTimeField()
    referrer = models.CharField(max_length=200)
    site_url = models.CharField(max_length=200)
    tab_referrer_url = models.CharField(max_length=200)
    http_method = models.CharField(max_length=100)
    by_ext_id = models.CharField(max_length=200)
    by_ext_name = models.CharField(max_length=200)
    mime_type = models.CharField(max_length=100)
    original_mime_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ChromeDownloadLogManager()

class ScreenshotManager(DesktopGlobalManager):
    def save_image(self, user, machine, path):
        desktop = self.__desktop(user, machine)
        self.create(desktop=desktop, path=path)
        return {"success": True}

class Screenshot(models.Model):
    desktop = models.ForeignKey(Desktop, null=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ScreenshotManager()
