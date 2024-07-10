import boto3
import json
import argparse

def invoke_sagemaker_endpoint(region, endpoint_name, payload):
    # Initialize the boto3 client for SageMaker
    sagemaker_client = boto3.client('sagemaker-runtime', region_name=region)

    # Invoke the endpoint
    response = sagemaker_client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',  # Specify the content type
        Body=json.dumps({"question": payload})
    )

    # Read the response
    result = response['Body'].read().decode('utf-8')
    print("Response from endpoint:", result)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Invoke a SageMaker endpoint')
    parser.add_argument('--region', type=str, required=True, help='AWS region where the SageMaker endpoint is deployed')
    parser.add_argument('--endpoint', type=str, required=True, help='Name of the SageMaker endpoint')
    parser.add_argument('--payload', type=str, required=True, help='Question to send to the endpoint')

    # Parse the arguments
    args = parser.parse_args()

    # Invoke the SageMaker endpoint
    invoke_sagemaker_endpoint(args.region, args.endpoint, args.payload)