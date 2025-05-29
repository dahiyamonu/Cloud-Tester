from django.db import models
import random
import string
import socket
import struct

def generate_serial():
    """Generates a unique serial number."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def generate_mac():
    """Generates a random MAC address."""
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)]).upper()

def generate_ip():
    """Generates a random IP address."""
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

class DeviceProfile(models.Model):
    serial_number = models.CharField(max_length=20, default=generate_serial)
    mac = models.CharField(max_length=100, default=generate_mac)  
    fw_info = models.CharField(max_length=50, default="AIROS-1.0.1-BUILD_23092024")
    hw_name = models.CharField(max_length=50, default="MTK7621")
    hw_version = models.CharField(max_length=10, default="1.0")
    mgmt_ip = models.GenericIPAddressField(default=generate_ip)
    egress_ip = models.GenericIPAddressField(default=generate_ip)

    def __str__(self):
        return f"Device {self.serial_number} ({self.mac})"

class Device(models.Model):
    serial_number = models.CharField(max_length=20, default=generate_serial)
    mac = models.CharField(max_length=100, default=generate_mac)  
    fw_info = models.CharField(max_length=100, default="AIROS-1.0.1-BUILD_23092024")
    hw_name = models.CharField(max_length=100, default="MTK7621")
    hw_version = models.CharField(max_length=100, default="1.0")
    mgmt_ip = models.GenericIPAddressField(default=generate_ip)
    egress_ip = models.GenericIPAddressField(default=generate_ip) 

    def __str__(self):
        return self.serial_number