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
