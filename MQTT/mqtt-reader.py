import paho.mqtt.client as mqtt
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    """Called when client connects to broker"""
    if rc == 0:
        logger.info("Successfully connected to MQTT broker")
        client.subscribe("rfid/tags")  # Subscribe to topic
        logger.info("Subscribed to rfid/tags")
    else:
        logger.error(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Called when message is received"""
    logger.info(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")

def on_publish(client, userdata, mid):
    """Called when message is published"""
    logger.info("Message published successfully")

# Create MQTT client
client = mqtt.Client()

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

try:
    # Connect to broker
    logger.info("Connecting to broker...")
    client.connect("localhost", 1883, 60)
    
    # Start network loop in background thread
    client.loop_start()
    
    # Wait for connection to establish
    time.sleep(2)
    
    # Publish a test message
    logger.info("Publishing test message...")
    client.publish("rfid/tags", "Test message from Python")
    
    # Keep script running
    logger.info("Listening for messages... (Press Ctrl+C to exit)")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    logger.info("Shutting down...")
    client.loop_stop()
    client.disconnect()
except Exception as e:
    logger.error(f"Error occurred: {e}")
    client.loop_stop()
    client.disconnect()



