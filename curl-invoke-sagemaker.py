#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <region> <endpoint_name> <payload_file>"
    exit 1
fi

# Variables
REGION=$1
ENDPOINT_NAME=$2
PAYLOAD_FILE=$3
DEBUG_LOG="debug.log"

# Check if the payload file exists
if [ ! -f "$PAYLOAD_FILE" ]; then
    echo "Error: Payload file '$PAYLOAD_FILE' not found!"
    exit 1
fi

# AWS CLI command to generate the necessary headers
aws sagemaker-runtime invoke-endpoint \
  --region $REGION \
  --endpoint-name $ENDPOINT_NAME \
  --body fileb://$PAYLOAD_FILE \
  --content-type application/json \
  --cli-binary-format raw-in-base64-out \
  --debug > $DEBUG_LOG 2>&1

# Check if the AWS CLI command was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to invoke AWS CLI command. Check $DEBUG_LOG for details."
    exit 1
fi

# Extract headers from the debug output
AUTHORIZATION=$(grep -oP '(?<=Authorization: ).*' $DEBUG_LOG)
X_AMZ_DATE=$(grep -oP '(?<=X-Amz-Date: ).*' $DEBUG_LOG)

# Check if the headers were successfully extracted
if [ -z "$AUTHORIZATION" ] || [ -z "$X_AMZ_DATE" ]; then
    echo "Error: Failed to extract necessary headers from $DEBUG_LOG."
    exit 1
fi

# Make the curl request
RESPONSE=$(curl -s -X POST https://runtime.sagemaker.$REGION.amazonaws.com/endpoints/$ENDPOINT_NAME/invocations \
  -H "Content-Type: application/json" \
  -H "X-Amz-Date: $X_AMZ_DATE" \
  -H "Authorization: $AUTHORIZATION" \
  --data @$PAYLOAD_FILE \
  -k)

# Check if the curl request was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to make the curl request."
    exit 1
fi

# Output the response
echo "Response from endpoint:"
echo "$RESPONSE"
