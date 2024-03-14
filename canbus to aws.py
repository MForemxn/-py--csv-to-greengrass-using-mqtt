import can
import logging
import sys
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Configure logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

# AWS IoT Parameters
host = "your-iot-endpoint.amazonaws.com"
root_ca_path = 'path_to_root_ca.pem'
certificate_path = 'path_to_certificate.pem.crt'
private_key_path = 'path_to_private_key.pem.key'

# Initialize MQTT Client
myMQTTClient = AWSIoTMQTTClient("clientId")
myMQTTClient.configureEndpoint(host, 8883)
myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

# Connect to AWS IoT
try:
    myMQTTClient.connect()
    logger.info("Connected to AWS IoT")
except Exception as e:
    logger.error(f"Failed to connect to AWS IoT: {e}")
    sys.exit(1)

# CAN Bus setup
try:
    bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
    logger.debug("CAN bus interface initialized")
except Exception as e:
    logger.error(f"Failed to initialize CAN bus interface: {e}")
    sys.exit(1)

# Read from CAN bus and publish to MQTT
try:
    for msg in bus:
        # Assuming msg.data is the payload you want to send
        # Convert CAN message to the format you need, e.g., a JSON string
        json_string = str(msg.data.hex())  # Simple example: convert data to hex string
        topic = "your/topic"
        if myMQTTClient.publish(topic, json_string, 0):
            logger.info(f"Message published to {topic}")
        else:
            logger.error(f"Failed to publish message to {topic}")
except KeyboardInterrupt:
    logger.info("Interrupted by user")
except Exception as e:
    logger.error(f"An error occurred while reading from CAN bus: {e}")

# Disconnect from AWS IoT
try:
    myMQTTClient.disconnect()
    logger.info("Disconnected from AWS IoT")
except Exception as e:
    logger.error(f"Failed to disconnect properly: {e}")
