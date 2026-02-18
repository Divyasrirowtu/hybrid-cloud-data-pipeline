import os
import json
import time
import boto3
from google.cloud import pubsub_v1

# -----------------------------
# LocalStack SQS Setup
# -----------------------------
sqs = boto3.client(
    "sqs",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

queue_url = "http://localhost:4566/000000000000/data-processing-queue"

# -----------------------------
# GCP Pub/Sub Setup
# -----------------------------
gcp_project_id = os.getenv("GCP_PROJECT_ID")
pubsub_topic = "localstack-events"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(gcp_project_id, pubsub_topic)

print("Bridge application started. Polling SQS...")

# -----------------------------
# Polling Loop
# -----------------------------
while True:
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )

    messages = response.get("Messages", [])
    if not messages:
        time.sleep(1)
        continue

    for message in messages:
        body = json.loads(message["Body"])
        print(f"Received message: {body}")

        # Extract S3 object content from event
        if "Records" in body:
            s3_object = body["Records"][0]["s3"]["object"]["key"]
            # For simplicity, we read the file from LocalStack S3
            s3 = boto3.client(
                "s3",
                endpoint_url="http://localhost:4566",
                aws_access_key_id="test",
                aws_secret_access_key="test",
                region_name="us-east-1"
            )
            obj = s3.get_object(Bucket="hybrid-cloud-bucket", Key=s3_object)
            data = obj["Body"].read().decode("utf-8")

            # Publish to GCP Pub/Sub
            future = publisher.publish(topic_path, data.encode("utf-8"))
            print(f"Published to Pub/Sub: {data}")

        # Delete message from SQS
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message["ReceiptHandle"]
        )
        print("Message deleted from SQS")
