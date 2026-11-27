import os
import boto3
import time
from PIL import Image

AWS_REGION = "ap-south-1"
BUCKET_NAME = os.environ["THUMBNAIL_BUCKET"]
QUEUE_URL = os.environ["THUMBNAIL_QUEUE_URL"]
TABLE_NAME = os.environ["THUMBNAIL_TABLE"]

s3 = boto3.client("s3", region_name=AWS_REGION)
sqs = boto3.client("sqs", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

def make_thumbnail(local_path, thumb_path):
    img = Image.open(local_path)
    img.thumbnail((128, 128))
    img.save(thumb_path)

def process_message(filename):
    local_original = f"/tmp/{filename}"
    local_thumb = f"/tmp/thumb_{filename}"

    s3.download_file(BUCKET_NAME, f"uploads/{filename}", local_original)
    make_thumbnail(local_original, local_thumb)
    s3.upload_file(local_thumb, BUCKET_NAME, f"thumbnails/{filename}")

    table.update_item(
        Key={"filename": filename},
        UpdateExpression="SET #s = :s, thumbnail_key = :t",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "done", ":t": f"thumbnails/{filename}"}

    )
    print(f"Processed: {filename}")

def run():
    print("Worker started. Polling SQS...")
    while True:
        response = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=1, WaitTimeSeconds=10)
        messages = response.get("Messages", [])
        for msg in messages:
            filename = msg["Body"]
            try:
                process_message(filename)
                sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg["ReceiptHandle"])
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        time.sleep(1)

if __name__ == "__main__":
    run()