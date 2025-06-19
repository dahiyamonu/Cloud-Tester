import requests, json
import paho.mqtt.client as mqtt


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
        self.call_api(data)
        print("Message received:", message.payload.decode())

    def connect(self):
        try:
            print(type(self.MQTT_BROKER), self.MQTT_PORT)
            self.client.connect(self.MQTT_BROKER, self.MQTT_PORT)
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
