import boto3
import os

# Initialize Boto3 clients for SageMaker and IAM
sagemaker_client = boto3.client('sagemaker')
iam_client = boto3.client('iam')

def list_sagemaker_models():
    # List SageMaker models
    response = sagemaker_client.list_models()

    models = response['Models']
    for model in models:
        model_name = model['ModelName']
        model_arn = model['ModelArn']
        
        # Describe model details
        model_details = sagemaker_client.describe_model(ModelName=model_name)
        container_uri = model_details['PrimaryContainer']['Image']
        
        print(f"Model: {model_name}")
        print(f"  ARN: {model_arn}")
        print(f"  Container: {container_uri}")
        
        # List endpoints associated with the model
        list_endpoints_for_model(model_name)

def list_endpoints_for_model(model_name):
    # List endpoints associated with the given model
    response = sagemaker_client.list_endpoints(ModelNameEquals=model_name)

    endpoints = response['Endpoints']
    if endpoints:
        print("  Endpoints:")
        for endpoint in endpoints:
            endpoint_name = endpoint['EndpointName']
            endpoint_arn = endpoint['EndpointArn']
            
            print(f"    - Name: {endpoint_name}")
            print(f"      ARN: {endpoint_arn}")
    else:
        print("  No endpoints found for this model.")

def main():
    # List all SageMaker models and associated endpoints
    list_sagemaker_models()

if __name__ == "__main__":
    main()
