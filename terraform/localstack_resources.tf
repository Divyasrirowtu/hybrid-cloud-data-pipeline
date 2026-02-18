# -------------------------
# S3 Bucket
# -------------------------
resource "aws_s3_bucket" "bucket" {
  bucket = "hybrid-cloud-bucket"
}

# -------------------------
# SQS Queue
# -------------------------
resource "aws_sqs_queue" "queue" {
  name = "data-processing-queue"
}

# -------------------------
# DynamoDB Table
# -------------------------
resource "aws_dynamodb_table" "table" {
  name         = "processed-records"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "recordId"

  attribute {
    name = "recordId"
    type = "S"
  }
}
