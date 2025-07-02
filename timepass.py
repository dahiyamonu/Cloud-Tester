
import requests, json
import paho.mqtt.client as mqtt
from automate.mqbroker import client_report_data
from automate.mqbroker import device_report_data
from automate.mqbroker import vif_report_data


class MQTTClient:
    def __init__(self, mqtt_username, mqtt_password, mqtt_broker, mqtt_port):
        self.mqtt_username = mqtt_username
        self.mqtt_password = mqtt_password
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT connection successful.")
        else:
            print("MQTT connection failed with code:", rc)

    def on_message(self, client, userdata, message):
        data = message.payload.decode()
        # Example: handle client report data request message
        if data == "fetch_client_report":
            self.publish_client_report()
        elif data == "fetch_device_report":
            self.publish_device_report()
        elif data == "fetch_vif_report":
            self.publish_vif_report()
        else:
            print("Message received:", data)

    def connect(self):
        try:
            print(type(self.mqtt_broker), self.mqtt_port)
            self.client.connect(self.mqtt_broker, self.mqtt_port)
            self.client.loop_start()
        except Exception as e:
            print("Failed to connect to MQTT broker:", e)

    def publish(self, topic, payload):
        try:
            self.client.publish(topic, json.dumps(payload), qos=2)
        except Exception as e:
            print("Failed to publish MQTT message:", e)

    def subscribe(self, topic):
        try:
            self.client.subscribe(topic)
        except Exception as e:
            print("Failed to subscribe to MQTT topic:", e)

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def fetch_client_report(self):
        """Fetch client report data using client_report_data module."""
        report = client_report_data.ioctl80211_jedi_client_fetch_dummy()
        return report

    def publish_client_report(self, topic="client/report"):
        """Publish client report data to MQTT topic."""
        report = self.fetch_client_report()
        # Convert report to dict or JSON serializable format
        report_dict = {
            "n_client": report.n_client,
            "record": [
                {
                    "macaddr": client_report_data.format_mac_address(client.macaddr),
                    "hostname": client.hostname,
                    "ipaddr": client.ipaddr,
                    "ssid": client.ssid,
                    "rx_bytes": client.rx_bytes,
                    "tx_bytes": client.tx_bytes,
                    "rssi": client.rssi,
                    "is_connected": client.is_connected,
                    "duration_ms": client.duration_ms,
                    "radio_type": client_report_data.get_radio_type_name(client.radio_type),
                    "channel": client.channel,
                }
                for client in report.record
            ],
        }
        self.publish(topic, report_dict)

    def fetch_device_report(self):
        """Fetch device report data using device_report_data module."""
        report = device_report_data.fill_dummy_device_report()
        return report

    def publish_device_report(self, topic="device/report"):
        """Publish device report data to MQTT topic."""
        report = self.fetch_device_report()
        # Convert report to dict or JSON serializable format
        report_dict = {
            "timestamp_ms": report.timestamp_ms,
            "load": report.record.load,
            "uptime": report.record.uptime,
            "mem_util": {
                "mem_total": report.record.mem_util.mem_total,
                "mem_used": report.record.mem_util.mem_used,
                "swap_total": report.record.mem_util.swap_total,
                "swap_used": report.record.mem_util.swap_used,
            },
            "cpu_util": {
                "cpu_util": report.record.cpu_util.cpu_util,
            },
            "fs_util": [
                {
                    "fs_type": fs.fs_type,
                    "fs_total": fs.fs_total,
                    "fs_used": fs.fs_used,
                }
                for fs in report.record.fs_util
            ],
        }
        self.publish(topic, report_dict)

    def fetch_vif_report(self):
        """Fetch VIF report data using vif_report_data module."""
        report = vif_report_data.dummy_get_vif_report_data()
        return report

    def publish_vif_report(self, topic="vif/report"):
        """Publish VIF report data to MQTT topic."""
        report = self.fetch_vif_report()
        # Convert report to dict or JSON serializable format
        report_dict = {
            "n_vif": report.n_vif,
            "vif": [
                {
                    "radio": vif.radio,
                    "ssid": vif.ssid,
                    "num_sta": vif.num_sta,
                    "uplink_mb": vif.uplink_mb,
                    "downlink_mb": vif.downlink_mb,
                }
                for vif in report.vif
            ],
            "n_radio": report.n_radio,
            "radio": [
                {
                    "band": radio.band,
                    "channel": radio.channel,
                    "txpower": radio.txpower,
                    "channel_utilization": radio.channel_utilization,
                }
                for radio in report.radio
            ],
        }
        self.publish(topic, report_dict)


import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin

from device.utils import generate_ip, generate_mac
from .models import Device 
from .resources import DeviceResource

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
        def register_device(device):
            if not device.serial_number:
                return (f"Device {device.id}", "warning", "Skipped: No serial number.")

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
                    device.mac = payload["mac"]
                    device.fw_info = payload["fw_info"]
                    device.hw_name = payload["hw_name"]
                    device.hw_version = payload["hw_version"]
                    device.mgmt_ip = payload["mgmt_ip"]
                    device.egress_ip = payload["egress_ip"]
                    device.device_id = data['deviceId']
                    device.config = data
                    device.save()
                    return (device.serial_number, "success", "Registered successfully.")
                else:
                    return (device.serial_number, "error", f"Failed: HTTP {response.status_code}")
            except Exception as e:
                return (device.serial_number, "error", f"Exception: {str(e)}")

        # Run registration in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(register_device, device) for device in queryset]
            for future in as_completed(futures):
                device_sn, status, msg = future.result()
                if status == "success":
                    messages.success(request, f"{device_sn}: {msg}")
                elif status == "warning":
                    messages.warning(request, f"{device_sn}: {msg}")
                else:
                    messages.error(request, f"{device_sn}: {msg}")




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

#  for device in queryset:


import paho.mqtt.client as mqtt
import json
from dataclasses import asdict

# Dummy data generators
from mqbroker.device_report_data import fill_dummy_device_report
from mqbroker.client_report_data import ioctl80211_jedi_client_fetch_dummy
from mqbroker.vif_report_data import dummy_get_vif_report_data

# Device config and MQTT topic strings
device_data = {
    "deviceId": "5006945829",
    "serialNumber": "AIRIP3BR53TL2IS",
    "username": "b2d04e02e675418abf691db817fb4c3a",
    "password": "7d4fed9e6b1f3ec47a68f2b3057a8302b7e1f4ce4a9575ffc71149d87e8debafb3c125053338b94067501d73eae7d2bf",
    "broker": "69.30.254.180",
    "port": "35930",
    "statsTopic": {
        "device": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/device",
        "client": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/client",
        "vif": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/vif",
        "neighbor": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/neighbor",
        "config": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/config",
        "cmdr": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/cmdr"
    }
}

BROKER = device_data["broker"]
PORT = int(device_data["port"])
CLIENT_ID = "publisher-client"
USER_NAME = "bluesyobsignates"
PASSWORD = "PNJxhzMX2jkRVBG3"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker.")
    else:
        print(f"❌ Failed to connect, return code {rc}")

# Setup MQTT client
client = mqtt.Client(CLIENT_ID)
client.username_pw_set(USER_NAME, PASSWORD)
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

# === Publish device data ===
device_report = fill_dummy_device_report()
device_payload = json.dumps(asdict(device_report), indent=4)
device_topic = device_data["statsTopic"]["device"]

result = client.publish(device_topic, device_payload, qos=2)
if result.rc == mqtt.MQTT_ERR_SUCCESS:
    print(f"✅ Sent device report to `{device_topic}`")
else:
    print(f"❌ Failed to publish to `{device_topic}`")

# === Publish client data ===
client_report = ioctl80211_jedi_client_fetch_dummy()
client_payload = json.dumps(asdict(client_report), indent=4)
client_topic = device_data["statsTopic"]["client"]

result = client.publish(client_topic, client_payload, qos=2)
if result.rc == mqtt.MQTT_ERR_SUCCESS:
    print(f"✅ Sent client report to `{client_topic}`")
else:
    print(f"❌ Failed to publish to `{client_topic}`")

# === Publish VIF data ===
vif_report = dummy_get_vif_report_data()
vif_payload = json.dumps(asdict(vif_report), indent=4)
vif_topic = device_data["statsTopic"]["vif"]

result = client.publish(vif_topic, vif_payload, qos=2)
if result.rc == mqtt.MQTT_ERR_SUCCESS:
    print(f"✅ Sent VIF report to `{vif_topic}`")
else:
    print(f"❌ Failed to publish to `{vif_topic}`")

client.loop_stop()
client.disconnect()


import paho.mqtt.client as mqtt
import json
import time
from dataclasses import asdict

# Import the function and class from your dummy report script
from mqbroker.device_report_data import fill_dummy_device_report  # adjust the filename if needed
# Import the function for dummy client report
from mqbroker.client_report_data import ioctl80211_jedi_client_fetch_dummy  # adjust if file/module name differs
# Import only the VIF report function
from mqbroker.vif_report_data import dummy_get_vif_report_data  # Update the path as needed

# Device info
device_data = {
    "deviceId": "5006945829",
    "serialNumber": "AIRIP3BR53TL2IS",
    "username": "b2d04e02e675418abf691db817fb4c3a",
    "password": "7d4fed9e6b1f3ec47a68f2b3057a8302b7e1f4ce4a9575ffc71149d87e8debafb3c125053338b94067501d73eae7d2bf",
    "broker": "69.30.254.180",
    "port": "35930",
    "statsTopic": {
        "device": {
            "serialNum": "AIR587BE92472BD",
            "deviceId": "1457309733",
            "macAddr": "587BE92472BD",
            "tms": 1750756430541,
            "data": {
                "system": {
                    "uptime": 383,
                    "downtime": 0,
                    "totalClient": 0,
                    "uplinkMb": 0,
                    "downlinkMb": 0,
                    "totalTrafficMb": 0
                },
                "memUtil": {
                    "memTotal": 248592,
                    "memUsed": 99836,
                    "swapTotal": 0,
                    "swapUsed": 0
                },
                "fsUtil": [
                    {
                        "fsType": "FS_TYPE_ROOTFS",
                        "fsTotal": 3136,
                        "fsUsed": 384
                    },
                    {
                        "fsType": "FS_TYPE_TMPFS",
                        "fsTotal": 124296,
                        "fsUsed": 412
                    }
                ],
                "cpuUtil": {
                    "cpuUtil": 1
                }
            }
        },
        "client": {
            "serialNum": "AIR587BE92472BD",
            "deviceId": "1457309733",
            "macAddr": "587BE92472BD",
            "tms": 1750749446732,
            "data": [
                {
                    "macAddress": "54:AF:97:6A:14:23",
                    "hostname": "auditor",
                    "ipAddress": "192.168.12.101",
                    "ssid": "air-net-20",
                    "isConnected": 0,
                    "durationMs": 6104000,
                    "channel": 48,
                    "band": "BAND5G",
                    "stats": {
                        "rxBytes": 1251126,
                        "txBytes": 249729,
                        "rssi": -48
                    }
                }
            ]
        },
        "vif": {
            "serialNum": "AIR587BE92472BD",
            "deviceId": "1457309733",
            "macAddr": "587BE92472BD",
            "tms": 1750756430703,
            "data": {
                "radio": [
                    {
                        "band": "BAND2G",
                        "channel": 3,
                        "txpower": 35,
                        "channel_utilization": 28
                    },
                    {
                        "band": "BAND5G",
                        "channel": 48,
                        "txpower": 85,
                        "channel_utilization": 15
                    }
                ],
                "vif": [
                    {
                        "radio": "BAND5G",
                        "ssid": "pro-net-20",
                        "statNumSta": 0,
                        "statUplinkMb": 0,
                        "statDownlinkMb": 0
                    },
                    {
                        "radio": "BAND5G",
                        "ssid": "air-net-20",
                        "statNumSta": 0,
                        "statUplinkMb": 0,
                        "statDownlinkMb": 0
                    },
                    {
                        "radio": "BAND2G",
                        "ssid": "pro-net-20",
                        "statNumSta": 0,
                        "statUplinkMb": 0,
                        "statDownlinkMb": 0
                    },
                    {
                        "radio": "BAND2G",
                        "ssid": "air-net-20",
                        "statNumSta": 0,
                        "statUplinkMb": 0,
                        "statDownlinkMb": 0
                    }
                ]
            }
        },
        "neighbor": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/neighbor",
        "config": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/config",
        "cmdr": "dev/to/cloud/5006945829/AIRIP3BR53TL2IS/cmdr"
    }
}
BROKER = device_data["broker"]
PORT = int(device_data["port"])
# TOPIC = device_data["statsTopic"]["device"]["client"]
CLIENT_ID = "publisher-client"
USER_NAME = "bluesyobsignates"
PASSWORD = "PNJxhzMX2jkRVBG3"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker.")
    else:
        print(f"❌ Failed to connect, return code {rc}")

# Setup MQTT client
client = mqtt.Client(CLIENT_ID)
client.username_pw_set(USER_NAME, PASSWORD)
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()


# === Publish device data ===
device_report = fill_dummy_device_report()
device_payload = json.dumps(asdict(device_report), indent=4)

device_topic = device_data["statsTopic"]["device"]
result = client.publish(device_topic, device_payload, qos=2)
if result[0] == 0:
    print(f"✅ Sent device report to `{device_topic}`")
else:
    print(f"❌ Failed to publish to `{device_topic}`")


# === Publish client data ===
client_report = ioctl80211_jedi_client_fetch_dummy()
client_payload = json.dumps(asdict(client_report), indent=4)

client_topic = device_data["statsTopic"]["client"]
result = client.publish(client_topic, client_payload, qos=2)
if result[0] == 0:
    print(f"✅ Sent client report to `{client_topic}`")
else:
    print(f"❌ Failed to publish to `{client_topic}`")


# === Publish VIF data ===
vif_report = dummy_get_vif_report_data()
vif_payload = json.dumps(asdict(vif_report), indent=4)

vif_topic = device_data["statsTopic"]["vif"]
result = client.publish(vif_topic, vif_payload, qos=2)
if result[0] == 0:
    print(f"✅ Sent VIF report to `{vif_topic}`")
else:
    print(f"❌ Failed to publish to `{vif_topic}`")


client.loop_stop()
client.disconnect()
