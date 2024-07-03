
import boto3
import json

# Initialize the SageMaker runtime client using the default configuration
client = boto3.client('runtime.sagemaker')

# Define the endpoint name of the SageMaker model you want to interact with
endpoint_name = 'your-model-endpoint-name'

# Example payload: replace this with the actual data format your model expects
payload = json.dumps({'key': 'value'})

# Function to invoke the SageMaker endpoint
def invoke_model(data):
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=data
    )
    # Output the response from the model
    print(response['Body'].read())

# Invoke the model with the example payload
invoke_model(payload)
