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
