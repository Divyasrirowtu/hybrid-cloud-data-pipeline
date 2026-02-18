import os
import json
from datetime import datetime
import psycopg2
import boto3

# -----------------------------
# Environment Variables
# -----------------------------
GCP_DB_HOST = os.getenv("CLOUDSQL_HOST")
GCP_DB_NAME = os.getenv("CLOUDSQL_DB")
GCP_DB_USER = os.getenv("CLOUDSQL_USER")
GCP_DB_PASSWORD = os.getenv("CLOUDSQL_PASSWORD")

DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", "http://host.docker.internal:4566")
DYNAMODB_TABLE = "processed-records"

# -----------------------------
# DynamoDB Client (LocalStack)
# -----------------------------
dynamodb = boto3.client(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

# -----------------------------
# Cloud SQL Connection Helper
# -----------------------------
def insert_to_cloudsql(record):
    conn = psycopg2.connect(
        host=GCP_DB_HOST,
        database=GCP_DB_NAME,
        user=GCP_DB_USER,
        password=GCP_DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO records (id, user_email, value, processed_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """,
        (record["recordId"], record["userEmail"], record["value"], record["processed_at"])
    )
    conn.commit()
    cursor.close()
    conn.close()

# -----------------------------
# Cloud Function Entry Point
# -----------------------------
def process_pubsub(event, context):
    """Triggered from a Pub/Sub message."""
    try:
        message_data = json.loads(base64.b64decode(event['data']).decode('utf-8'))
        print(f"Received message: {message_data}")

        # Add processed_at timestamp
        message_data["processed_at"] = datetime.utcnow().isoformat()

        # Insert into Cloud SQL
        insert_to_cloudsql(message_data)

        # Insert into LocalStack DynamoDB
        dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                "recordId": {"S": message_data["recordId"]},
                "userEmail": {"S": message_data["userEmail"]},
                "value": {"N": str(message_data["value"])},
                "processedAt": {"S": message_data["processed_at"]}
            }
        )
        print("Message processed successfully.")

    except Exception as e:
        print(f"Error processing message: {e}")
