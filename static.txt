
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
    },
    "payload":{
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
device_topic = device_data["statsTopic"]["device"]
device_payload = json.dumps(device_data["payload"]["device"])

result = client.publish(device_topic, device_payload, qos=2)
if result.rc == mqtt.MQTT_ERR_SUCCESS:
    print(f"✅ Sent device report to `{device_topic}`")
else:
    print(f"❌ Failed to publish to `{device_topic}`")

# === Publish client data ===
client_report = ioctl80211_jedi_client_fetch_dummy()
client_topic = device_data["statsTopic"]["client"]
client_payload = json.dumps(device_data["payload"]["client"])

result = client.publish(client_topic, client_payload, qos=2)
if result.rc == mqtt.MQTT_ERR_SUCCESS:
    print(f"✅ Sent client report to `{client_topic}`")
else:
    print(f"❌ Failed to publish to `{client_topic}`")

# === Publish VIF data ===
vif_report = dummy_get_vif_report_data()
vif_topic = device_data["statsTopic"]["vif"]
vif_payload = json.dumps(device_data["payload"]["vif"])

result = client.publish(vif_topic, vif_payload, qos=2)
if result.rc == mqtt.MQTT_ERR_SUCCESS:
    print(f"✅ Sent VIF report to `{vif_topic}`")
else:
    print(f"❌ Failed to publish to `{vif_topic}`")

client.loop_stop()
client.disconnect()
