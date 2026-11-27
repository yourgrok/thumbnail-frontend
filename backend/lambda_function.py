import os
import json
import boto3
import base64
import uuid

s3 = boto3.client("s3")
sqs = boto3.client("sqs")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["THUMBNAIL_TABLE"])

BUCKET_NAME = os.environ["THUMBNAIL_BUCKET"]
QUEUE_URL = os.environ["THUMBNAIL_QUEUE_URL"]

def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    # Handle status check: GET /?filename=xxx.jpg
    if method == "GET":
        filename = event.get("queryStringParameters", {}).get("filename")
        if not filename:
            return {"statusCode": 400, "body": json.dumps({"error": "filename required"})}
        response = table.get_item(Key={"filename": filename})
        item = response.get("Item")
        if not item:
            return {"statusCode": 404, "body": json.dumps({"error": "not found"})}
        return {"statusCode": 200, "body": json.dumps(item)}

    # Handle upload: POST with base64 file body
    if method == "POST":
        body = json.loads(event["body"])
        filename = body["filename"]
        file_content = base64.b64decode(body["file_base64"])


        s3.put_object(Bucket=BUCKET_NAME, Key=f"uploads/{filename}", Body=file_content)
        table.put_item(Item={"filename": filename, "status": "uploaded"})
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=filename)

        return {"statusCode": 200, "body": json.dumps({"message": "uploaded", "filename": filename})}

    return {"statusCode": 405, "body": json.dumps({"error": "method not allowed"})}