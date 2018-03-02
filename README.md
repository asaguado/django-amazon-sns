# Sending SMS messages with Amazon SNS and Python
**What is Amazon Simple Notification Service?**

[Amazon Simple Notification Service (Amazon SNS)](https://aws.amazon.com/sns/) is a web service that coordinates and manages the delivery or sending of messages to subscribing endpoints or clients. In Amazon SNS, there are two types of clients—publishers and subscribers—also referred to as producers and consumers. Publishers communicate asynchronously with subscribers by producing and sending a message to a topic, which is a logical access point and communication channel. Subscribers (i.e., web servers, email addresses, Amazon SQS queues, AWS Lambda functions) consume or receive the message or notification over one of the supported protocols (i.e., Amazon SQS, HTTP/S, email, SMS, Lambda) when they are subscribed to the topic. 

![Amazon Simple Notification Service (Amazon SNS](https://docs.aws.amazon.com/sns/latest/dg/images/sns-how-works.png)

## Step 1: API key + boto3

If you're already using AWS, you've probably jumped through these hoops. I'm not going to walk you through them, but just realize you need to figure out how to sign up for an AWS account and get some api keys.

The second part of this is [boto3](https://aws.amazon.com/sdk-for-python/), amazon's python sdk.

```
pip install boto3
```

Boto's [quickstart guide](https://boto3.readthedocs.io/en/latest/guide/quickstart.html) should help, and it also includes some info on getting boto configured.

## Step 2: Send your message

At the bare minimum, you can just send a message directly to a single phone number. Here's the code:

```
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
```

Note the formate of the phone number. It's got to be in something called [E.164 format](https://en.wikipedia.org/wiki/E.164). For US phone numbers, this includes the ```+1``` country code, then the area code + the rest of the phone number without any additional formatting.

If you just need to send a message every once in a while (e.g. to notifiy yourself when something happens), then congrats! You're done.

## Step 3: Do actual Pub-Sub

If you need to send messages to multiple recipients, it's worthwhile to read though Amazon's docs on [sending to multiple phone numbers](http://docs.aws.amazon.com/sns/latest/dg/sms_publish-to-topic.html).

The SNS service implements the [Publish-Subscribe](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) pattern, and you can use it to send messages to a topic. Here are the steps to make this work:

    Create a named topic. This is just a commuication channel to which you can subscribe phone numbers.
    Subscibe your recipients to the topic.
    Publish a message on the topic.

The python code looks something like this:

```
import boto3

# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id="YOUR ACCES KEY",
    aws_secret_access_key="YOUR SECRET KEY",
    region_name="us-east-1"
)

# Create the topic if it doesn't exist (this is idempotent)
topic = client.create_topic(Name="notifications")
topic_arn = topic['TopicArn']  # get its Amazon Resource Name

# Add SMS Subscribers
for number in some_list_of_contacts:
    client.subscribe(
        TopicArn=topic_arn,
        Protocol='sms',
        Endpoint=number  # <-- number who'll receive an SMS message.
    )

# Publish a message.
client.publish(Message="Good news everyone!", TopicArn=topic_arn)
```

All your susbscibers should recieve an SMS message once you've published it on the topic. In addition, you should be able to monitor SNS usage on the [AWS console](https://console.aws.amazon.com/), which will tell you how many messages are sent (as well as how many sms mesages fail). If you plan to use SNS for any commercial usage, you'll also want to read up on [SNS Pricing](https://aws.amazon.com/sns/pricing/).

Is there a way to set AWS.SNS.SMS.MaxPrice using boto3. AWS.SNS.SMS.MaxPrice as mentioned in [Sending an SMS Message](https://docs.aws.amazon.com/sns/latest/dg/sms_publish-to-phone.html). If you send the message programmatically by using the Amazon SNS API or AWS SDKs, you can specify a maximum price for the message delivery. 

Each SMS message can contain up to 140 bytes, and the character limit depends on the encoding scheme. For example, an SMS message can contain:

* 160 GSM characters
* 140 ASCII characters
* 70 UCS-2 characters

If you publish a message that exceeds the size limit, Amazon SNS sends it as multiple messages, each fitting within the size limit. Messages are not cut off in the middle of a word but on whole-word boundaries. The total size limit for a single SMS publish action is 1600 bytes. 

That's it! Hope this article has helped. Let me know in the comments below :)
