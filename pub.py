import paho.mqtt.client as mqtt
import json

# Example JSON with full data (you can load this from a file or variable)
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

BROKER = "69.30.254.180"  # or your MQTT broker address
PORT = 35930
TOPIC = "test/topic1235"
CLIENT_ID = "publisher-client"
USER_NAME = "bluesyobsignates"
PASSWORD = "PNJxhzMX2jkRVBG3"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker.")
    else:
        print(f"Failed to connect, return code {rc}")

client = mqtt.Client()
client.username_pw_set(USER_NAME, PASSWORD)
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

# Publish a message on each statsTopic
for topic_name, topic_path in device_data["statsTopic"].items():
    message = f"Test message to {topic_name}"
    result = client.publish(topic_path, message, qos=2)
    status = result[0]
    if status == 0:
        print(f"✅ Sent `{message}` to topic `{topic_path}`")
    else:
        print(f"❌ Failed to send message to topic {topic_path}")

# # Publish with QoS 2
# message = "Hello from Publisher 3 with QoS"
# client.publish(TOPIC, message)

client.loop_stop()
client.disconnect()
