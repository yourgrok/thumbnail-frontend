# Image Thumbnail Generator

UCS531 Cloud Computing project. Upload an image, queue it for background resizing, and check its status from the browser. [Open the deployed frontend](https://yourgrok.github.io/thumbnail-frontend/).

## Source code

| File | What it does |
| --- | --- |
| [index.html](index.html) | Browser interface that uploads images and polls for status. |
| [backend/lambda_function.py](backend/lambda_function.py) | Accepts uploads, stores originals in S3, queues jobs in SQS, and reads status from DynamoDB. |
| [backend/worker.py](backend/worker.py) | Polls SQS, generates thumbnails with Pillow, saves them to S3, and updates DynamoDB. |

The backend source was recovered from the implementation walkthrough. These copies take their AWS resource settings from environment variables.

## Setup and use

1. Configure `THUMBNAIL_BUCKET`, `THUMBNAIL_QUEUE_URL`, and `THUMBNAIL_TABLE` in both backend environments. The worker is configured for `ap-south-1`. The DynamoDB table uses a string partition key named `filename`.
2. Deploy the Lambda source with handler `lambda_function.lambda_handler`. Use its Function URL and allow the frontend origin through CORS for GET and POST with the Content-Type header. Give Lambda and EC2 IAM roles with access to the required S3, SQS, and DynamoDB resources.
3. From the repository root on EC2, install the worker dependencies using `python3 -m pip install boto3 Pillow`, then run `python3 backend/worker.py`.
4. Open the frontend, enter your Lambda Function URL, and choose a test JPG or PNG under about 4 MB. The browser shows **Queued** when Lambda accepts the upload and **Done** when the thumbnail is ready.

The browser displays the status and thumbnail object key. The images are stored in the private S3 bucket.
