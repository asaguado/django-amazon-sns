# An example of how to use AWS SNS with Python's boto
# By Alfredo Sanchez @asaguado
# Publish on March 2018
# http://aws.amazon.com/sns/
# https://boto3.readthedocs.io/en/latest/reference/services/sns.html
# https://docs.aws.amazon.com/sns/latest/api/API_Publish.html


import boto3


# AWS Credentials
AWS_ACCESS_KEY_ID = "<REPLACE_WITH_AWS_ACCESS_KEY_ID>"
AWS_SECRET_ACCESS_KEY = "<REPLACE_WITH_AWS_SECRET_ACCESS_KEY>"
AWS_REGION_NAME = "eu-west-1"

SENDER_ID = "<REPLACE_WITH_SENDER_ID>"
SMS_MOBILE = "<REPLACE_WITH_PHONE_NUMBER>"  # Make sure is set in E.164 format.
SMS_MESSAGE = "<REPLACE_WITH_MESSAGE>"


# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

# Send your sms message.
response = client.publish(
    PhoneNumber=SMS_MOBILE,
    Message=SMS_MESSAGE,
    MessageAttributes={
        'string': {
            'DataType': 'String',
            'StringValue': 'String',
        },
        'AWS.SNS.SMS.SenderID': {
            'DataType': 'String',
            'StringValue': SENDER_ID
        }
    }
)

print(response)
print("MessageId:" + response["MessageId"])
print("HTTPStatusCode:" + str(response["ResponseMetadata"]["HTTPStatusCode"]))