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


class Processor(models.Model):
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    base_frequency = models.CharField(max_length=100)
    cache = models.CharField(max_length=100)
    max_turbo_frequency = models.CharField(max_length=100)
    cores = models.IntegerField()
    threads = models.IntegerField()

class DisplayLaptop(models.Model):
    type = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    resolution = models.CharField(max_length=100)
    aspect_ratio = models.CharField(max_length=100)
    features = models.TextField(blank=True)


class MemoryLaptop(models.Model):
    configuration = models.CharField(max_length=100)
    max_capacity = models.CharField(max_length=100)


class KeyboardTouchPad(models.Model):
    type = models.CharField(max_length=100)
    key_travel = models.CharField(max_length=100)
    features = models.TextField(blank=False)



class CameraLaptop(models.Model):
    resolution = models.CharField(max_length=100)
    features = models.TextField(blank=False)



class NetworkCommunicationLaptop(models.Model):
    wifi = models.CharField(max_length=100)
    bluetooth = models.CharField(max_length=100)


class BatteryLaptop(models.Model):
    capacity = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    features = models.TextField(blank=False)


class MaterialsHeadset(models.Model):
    headband_cushion = models.CharField(max_length=100)
    ear_cushions = models.CharField(max_length=100)
    slider_arm = models.CharField(max_length=100)

class AdditionalFeaturesHeadset(models.Model):
    busy_light = models.CharField(max_length=100)
    controls = models.CharField(max_length=100)
    certifications = models.CharField(max_length=100)
    warranty = models.CharField(max_length=100)


class PhysicalSpecificationHeadset(models.Model):
    dimensions = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    materials = models.ForeignKey(MaterialsHeadset, on_delete=models.CASCADE)


class FrequencyResponseHeadset(models.Model):
    music_mode = models.CharField(max_length=100)
    speak_mode = models.CharField(max_length=100)


class MicrophoneHeadset(models.Model):
    type = models.CharField(max_length=100)
    noise_cancelling = models.BooleanField()
    frequency_range = models.CharField(max_length=100)


class AudioFeaturesHeadset(models.Model):
    speaker_size = models.CharField(max_length=100)
    frequency_response = models.ForeignKey(FrequencyResponseHeadset, on_delete=models.CASCADE)
    microphone = models.ForeignKey(MicrophoneHeadset, on_delete=models.CASCADE)
    hearing_protection = models.CharField(max_length=200)


class ConnectivityHeadset(models.Model):
    connection_type = models.CharField(max_length=100)
    cable_length = models.CharField(max_length=100)

class VideoWebcam(models.Model):
    max_resolution = models.CharField(max_length=100)
    frame_rate = models.CharField(max_length=100)
    field_of_view = models.CharField(max_length=100)
    focus_type = models.CharField(max_length=100)
    len_type = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=100)

class PhotoWebcam(models.Model):
    max_resolution = models.CharField(max_length=100)

class AudioWebcam(models.Model):
    microphone = models.CharField(max_length=100)

class FeaturesWebcam(models.Model):
    automatic_light_correction = models.CharField(max_length=100)
    video_effects = models.CharField(max_length=100)

class CompatibilityWebcam(models.Model):
    operating_system = models.CharField(max_length=100)
    software = models.CharField(max_length=100)


class HardwareWebcam(models.Model):
    connection_type = models.CharField(max_length=100)
    cable_length = models.CharField(max_length=100)
    mounting_clip = models.CharField(max_length=100)


class BasicSystemRequirementWebcam(models.Model):
    processor = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)


class HdVideoCallingSystemRequirementWebcam(models.Model):
    processor = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    usb_port = models.CharField(max_length=100)
    internet_upload_speed = models.CharField(max_length=100)
    screen_resolution = models.CharField(max_length=100)


class DimensionsWebcam(models.Model):
    weight = models.CharField(max_length=100)
    size = models.CharField(max_length=100)


class SystemRequirementsWebcam(models.Model):
    basic = models.ForeignKey(BasicSystemRequirementWebcam, on_delete=models.CASCADE)
    hd_video_calling = models.ForeignKey(HdVideoCallingSystemRequirementWebcam, on_delete=models.CASCADE)

class ActiveAreaDisplayMonitor(models.Model):
    width = models.CharField(max_length=100)
    height = models.CharField(max_length=100)

class ViewingAngleDisplayMonitor(models.Model):
    horizontal = models.CharField(max_length=100)
    vertical = models.CharField(max_length=100)

class ContrastRatioDisplayMonitor(models.Model):
    static = models.CharField(max_length=100)
    dynamic = models.CharField(max_length=100)

class DisplayMonitor(models.Model):
    size = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    viewable_image_area = models.CharField(max_length=100)
    active_area = models.ForeignKey(ActiveAreaDisplayMonitor, on_delete=models.CASCADE)
    resolution = models.CharField(max_length=100)
    aspect_ratio = models.CharField(max_length=100)
    viewing_angle = models.CharField(max_length=100)
    brightness = models.CharField(max_length=100)
    contrast_ratio = models.ForeignKey(ContrastRatioDisplayMonitor, on_delete=models.CASCADE)
    response_time = models.CharField(max_length=100)
    pixel_pitch = models.CharField(max_length=100)
    color_support = models.CharField(max_length=100)
    color_gamut = models.CharField(max_length=100)


class UserControlsMonitor(models.Model):
    buttons = models.TextField()
    languages = models.TextField()
    on_screen_display_controls = models.TextField()
    user_programmable_controls = models.CharField(max_length=100)

class SignalInterfacePerformanceMonitor(models.Model):
    horizontal_frequency = models.CharField(max_length=100)
    vertical_frequency = models.CharField(max_length=100)
    native_resolution = models.CharField(max_length=100)
    preset_graphic_modes = models.TextField()
    anti_glare = models.BooleanField()

class VideoOtherInputsMonitor(models.Model):
    plug_and_play = models.BooleanField()
    input_output_connectors = models.TextField()
    hdcp_support = models.CharField(max_length=100)
    video_cables_included = models.TextField()
    audio = models.CharField(max_length=100)

class PowerMonitor(models.Model):
    power_supply = models.CharField(max_length=100)
    maximum_power = models.CharField(max_length=100)
    typical_power = models.CharField(max_length=100)
    sleep_power = models.CharField(max_length=100)
    power_cable_length = models.CharField(max_length=100)

class ErgonomicFeaturesMonitor(models.Model):
    detachable_stand = models.BooleanField()
    height_adjustment = models.CharField(max_length=100)
    tilt_range = models.CharField(max_length=100)
    swivel = models.CharField(max_length=100)
    pivot = models.CharField(max_length=100)

class DimensionsMonitor(models.Model):
    width = models.CharField(max_length=100)
    height = models.CharField(max_length=100)
    depth = models.CharField(max_length=100)

class DimensionsKM(models.Model):
    height = models.CharField(max_length=100)
    width = models.CharField(max_length=100)
    depth = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    cable_length = models.CharField(max_length=100)

class FeaturesKeyboard(models.Model):
    spill_resistant = models.BooleanField()
    adjustable_tilt_legs = models.BooleanField()
    low_profile_keys = models.BooleanField()
    plug_and_play = models.BooleanField()

class FeaturesMouse(models.Model):
    ambidextrous_design = models.BooleanField()
    plug_and_play = models.BooleanField()


class PhysicalSpecificationMonitor(models.Model):
    dimensions = models.ForeignKey(DimensionsMonitor, on_delete=models.CASCADE)
    weight = models.CharField(max_length=100)

class EnvironmentalMonitor(models.Model):
    backlight_lamp_life = models.CharField(max_length=100)

class KeyboardKM(models.Model):
    dimensions = models.ForeignKey(DimensionsKM, on_delete=models.CASCADE)
    layout = models.CharField(max_length=100)
    key_lifespan = models.CharField(max_length=100)
    special_keys = models.TextField()
    features = models.ForeignKey(FeaturesKeyboard, on_delete=models.CASCADE)

class TrackingKM(models.Model):
    technology = models.CharField(max_length=100)
    resolution = models.CharField(max_length=100)

class MouseKM(models.Model):
    dimensions = models.ForeignKey(DimensionsKM, on_delete=models.CASCADE)
    tracking = models.ForeignKey(TrackingKM, on_delete=models.CASCADE)
    buttons = models.IntegerField()
    scroll_wheel = models.BooleanField()
    features = models.ForeignKey(FeaturesMouse, on_delete=models.CASCADE)

class ConnectivityKM(models.Model):
    type = models.CharField(max_length=100)
    interface = models.CharField(max_length=100)
    compatibility = models.TextField()

class LaptopSpec(models.Model):
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    operating_system = models.CharField(max_length=100)
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
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


class HeadsetSpec(models.Model):
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    audio_features = models.ForeignKey(AudioFeaturesHeadset, on_delete=models.CASCADE)
    connectivity = models.ForeignKey(ConnectivityHeadset, on_delete=models.CASCADE)
    physical_specifications = models.ForeignKey(PhysicalSpecificationHeadset, on_delete=models.CASCADE)
    additional_features = models.ForeignKey(AdditionalFeaturesHeadset, on_delete=models.CASCADE)


class WebcamSpec(models.Model):
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoWebcam, on_delete=models.CASCADE)
    photo = models.ForeignKey(PhotoWebcam, on_delete=models.CASCADE)
    audio = models.ForeignKey(AudioWebcam, on_delete=models.CASCADE)
    features = models.ForeignKey(FeaturesWebcam, on_delete=models.CASCADE)
    compatibility = models.ForeignKey(CompatibilityWebcam, on_delete=models.CASCADE)
    hardware = models.ForeignKey(HardwareWebcam, on_delete=models.CASCADE)
    system_requirements = models.ForeignKey(SystemRequirementsWebcam, on_delete=models.CASCADE)
    dimensions = models.ForeignKey(DimensionsWebcam, on_delete=models.CASCADE)

class MonitorSpec(models.Model):
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    display = models.ForeignKey(DisplayMonitor, on_delete=models.CASCADE)
    user_controls = models.ForeignKey(UserControlsMonitor, on_delete=models.CASCADE)
    signal_interface_performance = models.ForeignKey(SignalInterfacePerformanceMonitor, on_delete=models.CASCADE)
    video_other_inputs = models.ForeignKey(VideoOtherInputsMonitor, on_delete=models.CASCADE)
    ergonomic_features = models.ForeignKey(ErgonomicFeaturesMonitor, on_delete=models.CASCADE)
    whats_in_the_box = models.TextField()
    physical_specifications = models.ForeignKey(PhysicalSpecificationMonitor, on_delete=models.CASCADE)


class KMSpec(models.Model):
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    keyboard = models.ForeignKey(KeyboardKM, on_delete=models.CASCADE)
    mouse = models.ForeignKey(MouseKM, on_delete=models.CASCADE)
    connectivity = models.ForeignKey(ConnectivityKM, on_delete=models.CASCADE)
    warranty = models.CharField(max_length=100)


class Equipment(models.Model):
    model = models.ForeignKey(EquipmentBrandModel, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=150)
    notes = models.TextField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
