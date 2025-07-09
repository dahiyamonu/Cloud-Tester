import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime, timezone

# ========= Load Devices from Excel =========
EXCEL_PATH = "Device.xlsx"

def load_devices_from_excel(file_path):
    df = pd.read_excel(file_path)
    devices = df[["deviceId", "serialNumber"]].dropna().to_dict(orient="records")
    return devices

# ========= MQTT Broker Config =========
BROKER = "69.30.254.180"
PORT = 35930
CLIENT_ID = "publisher-client"
USER_NAME = "bluesyobsignates"
PASSWORD = "PNJxhzMX2jkRVBG3"

# ========= MQTT Event Handlers =========
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker.")
    else:
        print(f"❌ Failed to connect, return code {rc}")

# ========= Payload Generator =========
def generate_device_data(device_id, serial_number):
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    mac = "587BE92472BD"  # Can be randomized if needed

    stats_topic = {
        key: f"dev/to/cloud/{device_id}/{serial_number}/{key}"
        for key in ["device", "client", "vif", "neighbor", "config", "cmdr"]
    }

    payload = {
        "device": {
            "serialNumber": serial_number,
            "deviceId": device_id,
            "macAddr": mac,
            "tms": timestamp,
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
                    {"fsType": "FS_TYPE_ROOTFS", "fsTotal": 3136, "fsUsed": 384},
                    {"fsType": "FS_TYPE_TMPFS", "fsTotal": 124296, "fsUsed": 412}
                ],
                "cpuUtil": {"cpuUtil": 1}
            }
        },
        "client": {
            "serialNumber": serial_number,
            "deviceId": device_id,
            "macAddr": mac,
            "tms": timestamp,
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
            "serialNumber": serial_number,
            "deviceId": device_id,
            "macAddr": mac,
            "tms": timestamp,
            "data": {
                "radio": [
                    {"band": "BAND2G", "channel": 3, "txpower": 35, "channel_utilization": 28},
                    {"band": "BAND5G", "channel": 48, "txpower": 85, "channel_utilization": 15}
                ],
                "vif": [
                    {"radio": "BAND5G", "ssid": "pro-net-20", "statNumSta": 0, "statUplinkMb": 0, "statDownlinkMb": 0},
                    {"radio": "BAND5G", "ssid": "air-net-20", "statNumSta": 0, "statUplinkMb": 0, "statDownlinkMb": 0},
                    {"radio": "BAND2G", "ssid": "pro-net-20", "statNumSta": 0, "statUplinkMb": 0, "statDownlinkMb": 0},
                    {"radio": "BAND2G", "ssid": "air-net-20", "statNumSta": 0, "statUplinkMb": 0, "statDownlinkMb": 0}
                ]
            }
        }
    }

    return stats_topic, payload

# ========= MQTT Client Setup =========
client = mqtt.Client(CLIENT_ID)
client.username_pw_set(USER_NAME, PASSWORD)
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

# ========= Publish Data for All Devices =========
devices = load_devices_from_excel(EXCEL_PATH)

for device in devices:
    device_id = str(device["deviceId"])
    serial_number = str(device["serialNumber"])

    topics, payload = generate_device_data(device_id, serial_number)

    print(f"\n📡 Publishing for Device ID: {device_id}, SN: {serial_number}")
    for key in ["device", "client", "vif"]:
        topic = topics[key]
        message = json.dumps(payload[key])
        result = client.publish(topic, message, qos=2)

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"✅ Sent `{key}` report to `{topic}`")
        else:
            print(f"❌ Failed to publish `{key}` report to `{topic}`")

# ========= Cleanup =========
client.loop_stop()
client.disconnect()
print("\n🚀 All data published. Disconnected from broker.")
