# -*- coding: utf-8 -*-
import boto3

# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id="YOUR ACCES KEY",
    aws_secret_access_key="YOUR SECRET KEY",
    region_name="us-east-1"
)

# Send your sms message.
client.publish(
    PhoneNumber="+12223334444",
    Message="Hello World!"
)