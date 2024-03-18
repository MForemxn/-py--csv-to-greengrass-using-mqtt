import pandas as pd
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

# Parameters
csv_file_path = '/Users/masonforeman/Library/Mobile Documents/com~apple~CloudDocs/University/Other/UTS Motorsports/telemetry/Test Data/electric_race_car_telemetry.csv'
host = "avcujj6p3fbtu-ats.iot.ap-southeast-2.amazonaws.com"
root_ca_path = '/Users/masonforeman/Library/Mobile Documents/com~apple~CloudDocs/University/Other/UTS Motorsports/telemetry/Python Perms/AmazonRootCA1.pem'
certificate_path = '/Users/masonforeman/Library/Mobile Documents/com~apple~CloudDocs/University/Other/UTS Motorsports/telemetry/Python Perms/fb2ae5db5aade948dae670e9e23cc2dd0cf080327a252b4fc30290f83631bb02-certificate.pem.crt'
private_key_path = '/Users/masonforeman/Library/Mobile Documents/com~apple~CloudDocs/University/Other/UTS Motorsports/telemetry/Python Perms/fb2ae5db5aade948dae670e9e23cc2dd0cf080327a252b4fc30290f83631bb02-private.pem.key'

logger.debug("Starting script execution")

# Initialize MQTT Client
myMQTTClient = AWSIoTMQTTClient("iotconsole-38b09eb7-0661-4394-ae79-5e0a41e1f492")
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

# Read CSV file and publish data
try:
    data = pd.read_csv(csv_file_path)
    logger.debug("CSV file read successfully")

    # Convert DataFrame to JSON (adjust as necessary for your data structure)
    json_string = data.to_json()
    logger.debug("Data converted to JSON")

    # Publish message to MQTT topic
    topic = "$aws/things/mason_test_instance_Py_CSV_to_AWS_GreenGrass_using_MQTT_2/shadow/update/documents"
    if myMQTTClient.publish(topic, json_string, 0):
        logger.info(f"Message published to {topic}")
    else:
        logger.error(f"Failed to publish message to {topic}")
except pd.errors.EmptyDataError:
    logger.error("CSV file is empty or does not exist")
except pd.errors.ParserError:
    logger.error("Error parsing CSV file")
except Exception as e:
    logger.error(f"An error occurred: {e}")

# Disconnect
try:
    myMQTTClient.disconnect()
    logger.info("Disconnected from AWS IoT")
except Exception as e:
    logger.error(f"Failed to disconnect properly: {e}")

logger.debug("Script execution completed")
