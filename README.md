# Cloud-Based File Upload and Processing Pipeline

UCS531 Cloud Computing project. The [live demo](https://yourgrok.github.io/thumbnail-frontend/) uploads an image, queues a resize job and displays the resulting status.

- [Project proposal](docs/proposal.md)
- [System architecture](docs/architecture.md)
- [Cloud deployment and live demonstration](docs/deployment-demo.md)
- [Project report with screenshots](docs/project-report.pdf)

## Source code

- [index.html](https://github.com/yourgrok/thumbnail-frontend/blob/main/index.html) contains the deployed browser interface, file encoding, upload requests and status polling.
- [Lambda handler](backend/lambda_function.py) accepts a base64 image in a JSON POST and looks up status on GET.
- [EC2 worker](backend/worker.py) polls SQS, downloads the original, creates a thumbnail with Pillow, stores it and updates the status.

The backend files were recovered from the project’s implementation walkthrough. The AWS resource settings are supplied through environment variables in these copies. The deployed code remains in Lambda and on EC2.

## Run the class demo

Start the existing EC2 instance in Mumbai (ap-south-1) and run `python3 worker.py` in its terminal. Open the demo page, enter the existing Lambda Function URL and choose a fresh JPG or PNG under about 4 MB. The browser shows **Queued** after the API accepts the upload and **Done** after processing. See the deployment guide for verification and shutdown.

For a fresh setup, configure `THUMBNAIL_BUCKET`, `THUMBNAIL_QUEUE_URL` and `THUMBNAIL_TABLE` in both runtimes. Install the worker dependencies with `python3 -m pip install boto3 Pillow`. Use IAM execution roles for AWS access.
