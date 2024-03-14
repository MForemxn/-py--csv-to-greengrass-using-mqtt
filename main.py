import pandas as pd
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Parameters
csv_file_path = 'path_to_your_csv_file.csv'
host = "your-iot-endpoint.amazonaws.com"
root_ca_path = 'path_to_root_ca.pem'
certificate_path = 'path_to_certificate.pem.crt'
private_key_path = 'path_to_private_key.pem.key'

# Initialize MQTT Client
myMQTTClient = AWSIoTMQTTClient("clientId")
myMQTTClient.configureEndpoint(host, 8883)
myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

# Connect to AWS IoT
myMQTTClient.connect()

# Read CSV file
data = pd.read_csv(csv_file_path)

# Convert DataFrame to JSON (adjust as necessary for your data structure)
json_string = data.to_json()

# Publish message to MQTT topic
topic = "your/topic"
myMQTTClient.publish(topic, json_string, 0)

# Disconnect
myMQTTClient.disconnect()

