import boto3
import os

AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
REGION_NAME = "us-east-1"

class S3Client:

    s3_client = None
    s3_resource = None
    
    def __init__(self, region_name = REGION_NAME):

        if self.s3_resource is None or self.s3_client is None:
            __access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            __secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

            if __access_key_id is None:
                raise Exception(f"Environment Variable : {AWS_ACCESS_KEY_ID} is not set...")
            if __secret_access_key is None:
                raise Exception(f"Environment variable : {AWS_SECRET_ACCESS_KEY} is not set...")
            
            self.s3_resource = boto3.resource('s3', aws_access_key_id = __access_key_id, aws_secret_access_key = __secret_access_key, region_name = region_name)
            self.s3_client = boto3.client('s3', aws_access_key_id = __access_key_id, aws_secret_access_key = __secret_access_key, region_name = region_name)
