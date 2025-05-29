from django.shortcuts import render
import pandas as pd
import requests
from .models import Device
from django.core.files.storage import FileSystemStorage
import random
import string
import socket
import struct
import ipaddress

def generate_serial():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def generate_mac():
    return ':'.join(['{:02X}'.format(random.randint(0, 255)) for _ in range(6)])

def generate_ip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def is_valid_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def register_device(request):
    response_data = []
    error_message = None

    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        uploaded_file_path = fs.path(filename)

        try:
            df = pd.read_excel(uploaded_file_path)

            # Limit to first 50 rows
            # df = df.head(100)

            for index, row in df.iterrows():
                serial_number = row.get('serial_number') or generate_serial()
                mac = row.get('mac') or generate_mac()
                fw_info = row.get('fw_info') or "AIROS-1.0.1-BUILD_23092024"
                hw_name = row.get('hw_name') or "MTK7621"
                hw_version = row.get('hw_version') or "1.0"
                mgmt_ip = row.get('mgmt_ip') or generate_ip()
                egress_ip = row.get('egress_ip') or generate_ip()

                # Validate MAC
                if not isinstance(mac, str) or len(mac.split(':')) != 6:
                    mac = generate_mac()

                # Validate IPs
                if not is_valid_ip(mgmt_ip):
                    mgmt_ip = generate_ip()
                if not is_valid_ip(egress_ip):
                    egress_ip = generate_ip()

                device_data = {
                    'serial_number': str(serial_number),
                    'mac': mac.upper(),
                    'fw_info': str(fw_info),
                    'hw_name': str(hw_name),
                    'hw_version': str(hw_version),
                    'mgmt_ip': mgmt_ip,
                    'egress_ip': egress_ip
                }

                url = "http://69.30.254.180:8000/api/device_registration/v1/devices"

                try:
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(url, json=device_data, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    response_data.append(data)

                    Device.objects.create(
                        serial_number=device_data['serial_number'],
                        mac=device_data['mac'],
                        fw_info=device_data['fw_info'],
                        hw_name=device_data['hw_name'],
                        hw_version=device_data['hw_version'],
                        mgmt_ip=device_data['mgmt_ip'],
                        egress_ip=device_data['egress_ip']
                    )

                except requests.exceptions.RequestException as err:
                    error_message = f"Error on row {index + 2}: {err}"
                    continue

        except Exception as e:
            error_message = f"Failed to process Excel file: {e}"

    return render(request, 'cloud_data.html', {
        'response_data': response_data,
        'error_message': error_message,
    })
