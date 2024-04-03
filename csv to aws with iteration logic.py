import pandas as pd
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import sys
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

# Parameters

# Path to Data
csv_file_path = '/path/to/your/file.csv'

# AWS IoT Core endpoint
host = "your-iot-endpoint.amazonaws.com"

# Path to the root CA file
root_ca_path = '/path/to/your/downloads/AmazonRootCA1.pem'

# Path to the device certificate file
certificate_path = '/path/to/your/downloads/python-device.cert.pem'

# Path to the private key file
private_key_path = '/path/to/your/downloads/python-device.private.key'

logger.debug("Starting script execution")

# Initialize MQTT Client
myMQTTClient = AWSIoTMQTTClient("uniqueClientIdentifier")  # Make sure to provide a unique identifier for your client
myMQTTClient.configureEndpoint(host, 8883)
myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

logger.debug("MQTT client configured")

# Connect to AWS IoT
try:
    myMQTTClient.connect()
    logger.info("Connected to AWS IoT")
except Exception as e:
    logger.error(f"Failed to connect to AWS IoT: {e}")
    sys.exit(1)

logger.debug("Attempting to read and process CSV file")

# Function to send individual row data
def send_row_data(mqtt_client, topic, row_data):
    try:
        json_data = json.dumps(row_data)
        mqtt_client.publish(topic, json_data, 0)
        logger.info(f"Published data to {topic}: {json_data}")
    except Exception as e:
        logger.error(f"Error publishing data: {e}")

# Read CSV file and publish data row by row
try:
    data = pd.read_csv(csv_file_path)
    logger.debug("CSV file read successfully")

    topic = "$aws/things/your_thing_name/shadow/update"  # Replace with your actual MQTT topic

    # Process and send each row individually
    for index, row in data.iterrows():
        send_row_data(myMQTTClient, topic, row.to_dict())

except pd.errors.EmptyDataError:
    logger.error("CSV file is empty or does not exist")
except pd.errors.ParserError:
    logger.error("Error parsing CSV file")
except Exception as e:
    logger.error(f"An error occurred: {e}")

# Disconnect from AWS IoT
try:
    myMQTTClient.disconnect()
    logger.info("Disconnected from AWS IoT")
except Exception as e:
    logger.error(f"Failed to disconnect properly: {e}")

logger.debug("Script execution completed")
