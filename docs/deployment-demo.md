# Cloud deployment and demonstration

## Deployed components

The frontend is hosted on [GitHub Pages](https://yourgrok.github.io/thumbnail-frontend/). The AWS components operate in Mumbai (`ap-south-1`). Use the existing Function URL from the Lambda console for the public class demo.

| Component | Configuration |
| --- | --- |
| S3 | Private bucket. Keep original images under `uploads/` and thumbnails under `thumbnails/`. |
| SQS | Standard queue. Each message body is the job filename. |
| DynamoDB | String partition key `filename`. Items store `status` and, after processing, `thumbnail_key`. |
| Lambda | Python handler `lambda_function.lambda_handler`. Use its Function URL and configure CORS for the frontend origin with GET and POST and the Content-Type header. |
| EC2 | Python worker with boto3 and Pillow. The instance role can read originals, write thumbnails, receive/delete queue messages and update metadata. |
| Lambda role | Permit original writes to S3, SendMessage on the queue and PutItem/GetItem on the table, plus logging permissions. |

For a fresh deployment, create the storage, queue and table, configure the environment variables in the README and copy each backend file into its corresponding runtime. The class Function URL setup described in the walkthrough uses unauthenticated requests. Use test images for that endpoint.

## Live demonstration

1. Start the EC2 instance and connect. Leave the worker paused for the first upload.
2. Open the frontend, enter the Lambda Function URL and select a fresh JPEG under about 4 MB. Wait for **Queued**.
3. Show the original in S3 and the DynamoDB item with `status=uploaded`. Check the queue's available-message metric if needed. It is approximate. Receiving a message in the console can temporarily hide it from the worker.
4. Start `python3 worker.py`. Show the `Processed:` line and the browser changing to **Done**.
5. Show the thumbnail object and the corresponding `thumbnail_key`. The webpage displays the key and the completion mark. S3 access remains private.
6. Stop the worker with Ctrl+C and stop the EC2 instance after the demo.

If the upload fails with HTTP 413, try a smaller image. Base64 increases the request size. If it stays queued, check whether the instance and worker are running and inspect worker output for AWS access or image errors.

## Recorded evidence

- [Live upload interface](evidence/frontend.jpg)
- [Live Lambda response for the prior successful test job](evidence/completed.jpg)
