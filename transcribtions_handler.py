import json
import boto3 
import urllib3


def lambda_handler(event, context):
    for item_event in event["Records"]:
        item_event_body = json.loads(item_event["body"])
    
        job_name = item_event_body["job_guid"]
        url = item_event_body["audio_url"]
        
        bucket = "voice-recognition-213123"
        key = f"uploaded_files/{job_name}.mp3"
        s3_url = f"s3://{bucket}/{key}"
    
        s3=boto3.client('s3')
        http=urllib3.PoolManager()
        
        k = s3.upload_fileobj(http.request("GET", url,preload_content=False), bucket, key)
    
        client = boto3.client("transcribe")
    
        recognition_job = client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode="en-US",
            MediaFormat=url.split(".")[-1],
            Media={
                "MediaFileUri": s3_url,
            },
            OutputBucketName = bucket
        )
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("Transcribtions")
        table.put_item(
            Item={
                "pk": job_name,
                "audio_url": url,
                "transcription_url": key,
                "sentences": item_event_body["sentences"]
            }
        )
    
    return True
 
