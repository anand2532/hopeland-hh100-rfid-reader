import paho.mqtt.client as mqtt
import json
from datetime import datetime
class RFIDTagTracker:
    def init(self):
        self.tags = {}
        self.total_reads = 0
    def update_tag(self, tag):
        epc = tag['epc']
        device_timestamp = datetime.strptime(tag['timestamp'], '%Y-%m-%d %H:%M:%S.%f')

        # Increment total reads
        self.total_reads += 1

        if epc not in self.tags:
            
            self.tags[epc] = {
                'epc': epc,
                'first_timestamp': device_timestamp,
                'last_timestamp': device_timestamp,
                'count': 1,
                'latest_rssi': tag['rssi'],
                'antenna': tag['ant'],
                'serialno': tag['serialno']
            }
        else:
            # Update existing tag
            tag_info = self.tags[epc]
            tag_info['count'] += 1
            tag_info['last_timestamp'] = device_timestamp
            tag_info['latest_rssi'] = tag['rssi']
    def get_tag_report(self):
        return {
            'total_reads': self.total_reads,
            'total_unique_tags': len(self.tags),
            'tags': list(self.tags.values())
        }
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to MQTT Broker")
    client.subscribe("rfid/tags")
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        tracker = client.rfid_tracker
        # Handle both single tag and multiple tags
        tags = payload if isinstance(payload, list) else [payload]

        # Update tags
        for tag in tags:
            tracker.update_tag(tag)
        # Get and print current tag report
        report = tracker.get_tag_report()
        print("\nReal-time RFID Tag Status:")
        print(json.dumps(report, indent=2, default=str))
        print("-" * 60)
    except Exception as e:
        print(f"Error processing message: {e}")
def main():
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.rfid_tracker = RFIDTagTracker()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect("localhost", 1883)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nExiting...")
        client.disconnect()
    except Exception as e:
        print(f"Connection error: {e}")
if __name__ == "main":
    main()