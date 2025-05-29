from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from faker import Faker
import random
import string
from .models import Device
import openpyxl
from openpyxl.utils import get_column_letter
import os
from django.conf import settings

fake = Faker()

def generate_serial():
    return "AIR" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def generate_mac():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def generate_dummy_data(request):
    num_records = int(request.GET.get('num', 100))
    data = []

    for _ in range(num_records):
        record = {
            "serial_number": generate_serial(),
            "mac": generate_mac(),
            "fw_info": "AIROS-1.0.1-BUILD_23092024",
            "hw_name": "MTK7621",
            "hw_version": "1.0",
            "mgmt_ip": generate_ip(),
            "egress_ip": generate_ip()
        }

        # Save to DB
        Device.objects.create(**record)
        data.append(record)



    # Write to Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dummy Data"

    headers = list(data[0].keys())
    ws.append(headers)

    for record in data:
        ws.append(list(record.values()))

    # Inside generate_dummy_data
    excel_filename = "dummy_data.xlsx"
    media_dir = settings.MEDIA_ROOT

    # ✅ Create media directory if it doesn't exist
    os.makedirs(media_dir, exist_ok=True)

    file_path = os.path.join(settings.MEDIA_ROOT, excel_filename)
    wb.save(file_path)

    return render(request, 'data.html', {
        'data': data,
        'download_link': os.path.join(settings.MEDIA_URL, excel_filename)
    })
