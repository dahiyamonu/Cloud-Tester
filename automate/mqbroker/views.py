import json
from django.shortcuts import render
from dataclasses import asdict
from .device_report_data import fill_dummy_device_report  # Assuming the function is in device_report.py
from .client_report_data import ioctl80211_jedi_client_fetch_dummy
from .vif_report_data import ioctl80211_jedi_client_fetch_dummy, dummy_get_vif_report_data  # adjust as needed


def import_devices_view(request):
    # Generate device report
    device_data = fill_dummy_device_report()
    
    # Convert to JSON-compatible dict
    device_json_data = json.dumps(asdict(device_data), indent=4)
    
    # Pass it to the template
    return render(request, 'mqbroker/render_data.html', {
        'device_json': device_json_data
    })

def import_clients_view(request):
    # Generate dummy client report
    client_report = ioctl80211_jedi_client_fetch_dummy()
    
    # Convert dataclass to JSON-compatible dict
    client_json = json.dumps(asdict(client_report), indent=4)
    
    # Render to template
    return render(request, 'mqbroker/client_render.html', {
        'client_json': client_json
    })

def import_full_wifi_view(request):
    client_data = ioctl80211_jedi_client_fetch_dummy()
    vif_data = dummy_get_vif_report_data()

    context = {
        "client_json": json.dumps(asdict(client_data), indent=4),
        "vif_json": json.dumps(asdict(vif_data), indent=4),
    }

    return render(request, "mqbroker/vif_render.html", context)