import json
import boto3
import uuid


def lambda_handler(event, context):
    event_body = json.loads(event["body"])
    job_guid = str(uuid.uuid4())
    event_body["job_guid"] = job_guid
    
    if event_body["audio_url"].split(".")[-1] in ("mp3", "wav"):

        sqs = boto3.resource("sqs")
        queue = sqs.get_queue_by_name(QueueName="voice_re_sqs")
        
        queue.send_message(MessageBody=json.dumps(event_body))
        
        result = {
            "body": {
                "request_id": job_guid,
                "message": "Your request was accepted successfully"
            }
            
        }
    
        return result
    else:
        return {
            "body": {
                "request_id": None,
                "message": "The format of file have to be ,mp3 or .wav"
            }
            
        }
