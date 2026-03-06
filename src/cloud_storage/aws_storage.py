import boto3
from src.configuration.aws_connection import S3Client
from io import StringIO
from typing import Union, List
import os
import sys
from src.logger import logging
from src.exception import MyException
from botocore.exceptions import ClientError
from pandas import DataFrame, read_csv
import pickle
from mypy_boto3_s3.service_resource import Bucket


class SimpleStorageService:

    def __init__(self):

        client = S3Client()
        self.s3_resource = client.s3_resource
        self.s3_client = client.s3_client

    def s3_key_path_available(self, bucket_name, s3_key) -> bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            return len(file_objects) > 0
        except Exception as e:
            raise MyException(e, sys)
        
    def get_bucket(self, bucket_name : str) -> Bucket:
        logging.info("enter the get_bucket method of Simple Storage Service class!!!")

        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            return bucket
        except Exception as e:
            raise MyException(e, sys)
        
    def load_model(self, model_name : str, bucket_name : str, model_dir : str = None) -> object:

        try:
            model_file = model_dir + "/" + model_name if model_dir else model_name
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            model =  pickle.loads(model_obj)
            return model
        except Exception as e:
            raise MyException(e, sys)
    
    def get_file_object(self, filename : str, bucket_name : str) -> Union[List[object], object]:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(filename)]
            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(file_objects)
            return file_objs
        except Exception as e:
            raise MyException(e, sys) from e

    def upload_file(self, from_filename : str, to_filename : str, bucket_name : str, remove : bool = True):
        try:
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)

            if remove:
                os.remove(from_filename)
        except Exception as e:
            raise MyException(e, sys)