

# Hybrid Cloud Data Pipeline

## Overview
This project implements a hybrid data pipeline connecting LocalStack (AWS simulation) with Google Cloud Platform (GCP).  
It demonstrates a real-world multi-cloud architecture with Terraform as Infrastructure as Code, event-driven design, and cross-cloud synchronization.

## Architecture
1. **LocalStack S3**: Stores JSON files
2. **SQS Queue**: Receives S3 upload events
3. **Bridge Application**: Polls SQS → Publishes to GCP Pub/Sub
4. **GCP Cloud Function**: Processes Pub/Sub messages
5. **Cloud SQL**: Stores processed data
6. **LocalStack DynamoDB**: Stores processed data as backup

## Prerequisites
- Docker
- Terraform
- AWS CLI
- gcloud CLI
- Python 3.9+

## Setup Steps
1. Configure environment variables (`.env`)
2. Run `docker-compose up --build`
3. Apply Terraform:  
   ```powershell
   cd terraform
   terraform init
   terraform apply -auto-approve

4.Upload test JSON to S3:
awslocal s3 cp test-event.json s3://hybrid-cloud-bucket/

5.Monitor bridge logs to see Pub/Sub publish

6.Verify Cloud SQL and DynamoDB for processed data

Submission Files:

.env.example
submission.json
docker-compose.yml
Dockerfile
terraform/ folder
src/ folder

Authors:
Divya Sri Rowtu


---

# 🖥️ 2️⃣ Update `.gitignore`

Ensure you are ignoring sensitive and temporary files:


---

# 🖥️ 3️⃣ Clean Temporary Files

```powershell
Remove-Item *.log
Remove-Item *.pyc
