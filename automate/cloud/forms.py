from django import forms

class DeviceRegistrationForm(forms.Form):
    serial_number = forms.CharField(label="Serial Number", max_length=100)
    mac = forms.CharField(label="MAC Address", max_length=100)
    fw_info = forms.CharField(label="Firmware Info", max_length=100)
    hw_name = forms.CharField(label="Hardware Name", max_length=100)
    hw_version = forms.CharField(label="Hardware Version", max_length=100)
    mgmt_ip = forms.GenericIPAddressField(label="Management IP")
    egress_ip = forms.GenericIPAddressField(label="Egress IP")
