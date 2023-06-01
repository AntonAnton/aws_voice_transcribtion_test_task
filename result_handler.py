import json
import boto3

def lambda_handler(event, context):
    #  this lambda triggers by s3 create object events
    
    for event_item in event["Records"]:
        transcribtion_name = event_item["object"].split(".")[0]
        
        client = boto3.client("transcribe")
        transcribtion_res = client.get_transcription_job(
            TranscriptionJobName=transcribtion_name
        )
        
        db_record = table.get_item(
            Key={
                'pk': transcribtion_name,
            }
        )
        item = response['Item']
        
        for sentence in item["sentences"]:
            #  parse the transcription and find substrings
            pass
        
        #  make result and put into db
                
    return True
