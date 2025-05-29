from django.db import models

class Device(models.Model):
    """Model representing a device with a unique serial number."""
    
    name = models.CharField(max_length=255, verbose_name="Device Name")
    serial_number = models.CharField(max_length=255, unique=True, verbose_name="Serial Number")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        ordering = ["-created_at"]  # Orders by newest devices first
        verbose_name = "Device"
        verbose_name_plural = "Devices"

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
