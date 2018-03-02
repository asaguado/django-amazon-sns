# -*- coding: utf-8 -*-
import boto3

# AWS Credentials
AWS_ACCESS_KEY_ID = "YOUR ACCES KEY"
AWS_SECRET_ACCESS_KEY = "YOUR SECRET KEY"
AWS_REGION_NAME = "eu-west-1"

# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

# Send your sms message.
client.publish(
    PhoneNumber="+12223334444",
    Message="Hello World!"
)