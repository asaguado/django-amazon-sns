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

# Create the topic if it doesn't exist (this is idempotent)
topic = client.create_topic(Name="notifications")
topic_arn = topic['TopicArn']  # get its Amazon Resource Name

some_list_of_contacts = [
    '+12223334444',
    '+12223334445',
    '+12223334446',
]

# Add SMS Subscribers
for number in some_list_of_contacts:
    client.subscribe(
        TopicArn=topic_arn,
        Protocol='sms',
        Endpoint=number  # <-- number who'll receive an SMS message.
    )

# Publish a message.
client.publish(Message="Good news everyone!", TopicArn=topic_arn)