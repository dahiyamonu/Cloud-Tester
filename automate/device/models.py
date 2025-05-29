from django.db import models

# Create your models here.
class Device(models.Model):

    serial_number = models.CharField(max_length=100)
    alias = models.CharField(max_length=100, null=True, blank=True)
    device_id = models.CharField(max_length=100, null=True, blank=True)
    fw_info = models.CharField(max_length=100, null=True, blank=True)
    hw_name = models.CharField(max_length=100, null=True, blank=True)
    hw_version = models.CharField(max_length=100, null=True, blank=True)
    mac = models.CharField(max_length=50, null=True, blank=True)
    mgmt_ip = models.GenericIPAddressField(null=True, blank=True)
    egress_ip = models.GenericIPAddressField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return f"{self.serial_number} ------{self.device_id}"
