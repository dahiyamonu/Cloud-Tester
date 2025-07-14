import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime, timezone
import random

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

# ========= MAC and IP Generators =========
def random_mac():
    return ":".join(f"{random.randint(0x00, 0xFF):02X}" for _ in range(6))

def random_ip():
    return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"

def random_hostname():
    return random.choice(["router", "sensor", "gateway", "auditor", "iot-device"])

def random_ssid():
    return random.choice(["air-net-20", "pro-net-20", "iot-net", "test-net"])

# ========= Payload Generator =========
def generate_device_data(device_id, serial_number):
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    mac = random_mac()

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
                    "uptime": random.randint(100, 10000),
                    "downtime": random.randint(0, 500),
                    "totalClient": random.randint(0, 10),
                    "uplinkMb": random.randint(0, 50),
                    "downlinkMb": random.randint(0, 50),
                    "totalTrafficMb": random.randint(0, 100)
                },
                "memUtil": {
                    "memTotal": 248592,
                    "memUsed": random.randint(50000, 248592),
                    "swapTotal": 0,
                    "swapUsed": 0
                },
                "fsUtil": [
                    {"fsType": "FS_TYPE_ROOTFS", "fsTotal": 3136, "fsUsed": random.randint(200, 3136)},
                    {"fsType": "FS_TYPE_TMPFS", "fsTotal": 124296, "fsUsed": random.randint(100, 124296)}
                ],
                "cpuUtil": {"cpuUtil": random.randint(1, 90)}
            }
        },
        "client": {
            "serialNumber": serial_number,
            "deviceId": device_id,
            "macAddr": mac,
            "tms": timestamp,
            "data": [
                {
                    "macAddress": random_mac(),
                    "hostname": random_hostname(),
                    "ipAddress": random_ip(),
                    "ssid": random_ssid(),
                    "isConnected": random.choice([0, 1]),
                    "durationMs": random.randint(10000, 10000000),
                    "channel": random.choice([1, 6, 11, 36, 48]),
                    "band": random.choice(["BAND2G", "BAND5G"]),
                    "stats": {
                        "rxBytes": random.randint(1000, 1000000),
                        "txBytes": random.randint(1000, 1000000),
                        "rssi": random.randint(-80, -30)
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
                    {"band": "BAND2G", "channel": 3, "txpower": random.randint(10, 100), "channel_utilization": random.randint(5, 80)},
                    {"band": "BAND5G", "channel": 48, "txpower": random.randint(10, 100), "channel_utilization": random.randint(5, 80)}
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
