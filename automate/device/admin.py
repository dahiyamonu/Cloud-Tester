import requests
from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin

from device.utils import generate_ip, generate_mac
from .models import Device 
from .resources import DeviceResource
# Register your models here.


@admin.register(Device)
class DeviceAdmin(ImportExportModelAdmin):
    resource_class = DeviceResource
    list_display = (
        'serial_number',
        'alias',
        'device_id',
        'fw_info',
        'hw_name',
        'hw_version',
        'mac',
        'mgmt_ip',
        'egress_ip',
    )
    actions = ['register_selected_devices']
    @admin.action(description="Register selected devices to cloud")
    def register_selected_devices(self, request, queryset):
        for device in queryset:
            if not device.serial_number:
                messages.warning(request, f"Device {device.id} skipped: No serial number.")
                continue

            payload = {
                "serial_number": device.serial_number,
                "mac": generate_mac(),
                "fw_info": "AIROS-1.0.1-BUILD_23092024",
                "hw_name": "MTK7621",
                "hw_version": "1.0",
                "mgmt_ip": generate_ip(),
                "egress_ip": generate_ip(),
            }

            try:
                response = requests.post(
                    "http://69.30.254.180:8000/api/device_registration/v1/devices",
                    json=payload,
                    timeout=5,
                )
                if response.status_code == 200:
                    data = response.json()
                    print("Device registered successfully",  data['deviceId'])
                    device.mac = payload["mac"]
                    device.fw_info = payload["fw_info"]
                    device.hw_name = payload["hw_name"]
                    device.hw_version = payload["hw_version"]
                    device.mgmt_ip = payload["mgmt_ip"]
                    device.egress_ip = payload["egress_ip"]
                    device.device_id = data['deviceId']
                    device.config = data
                    device.save()
                    messages.success(request, f"Device {device.serial_number} registered.")
                else:
                    messages.error(request, f"Failed to register {device.serial_number}: {response.status_code}")
            except Exception as e:
                messages.error(request, f"Error for {device.serial_number}: {str(e)}")