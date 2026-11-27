# Project proposal

## Cloud-Based File Upload and Processing Pipeline

### Problem statement

A web application that resizes each image inside its upload request must keep that request open until the thumbnail is ready. When several photos arrive together, image processing can delay acknowledgement. The user needs to know when the original has been accepted and when the resulting thumbnail is ready.

### Objectives

1. Accept a browser upload and retain its original bytes in private cloud storage.
2. Return an acknowledgement after storing the original, recording its state and queuing the job.
3. Generate an aspect-ratio-preserving thumbnail within a 128 × 128 pixel box in a separate Python process.
4. Persist the processing status and output object key so the browser can check progress independently.
5. Demonstrate the split by accepting an upload while the worker is stopped and completing that same job after the worker starts.

### Scope and success criteria

The prototype covers image upload, background resizing and status tracking. Its browser demo shows the status and output key. The original and thumbnail can be inspected in the S3 console. A successful demo shows one fresh test image move from **Queued** to **Done**, with a corresponding status record and a thumbnail object.
