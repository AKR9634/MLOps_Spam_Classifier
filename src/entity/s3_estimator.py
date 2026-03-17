from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import Trained_Complete_Model
import sys
from pandas import DataFrame


class Cloud_Saved_Model:
    """
        This class is used to save and retrieve our model from s3 bucket and do prediction...
    """

    def __init__(self, bucket_name, model_path, ):
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: Trained_Complete_Model = None

    
    def is_model_present(self, model_path):
        try:
            return self.s3.s3_key_path_available(self.bucket_name, model_path)
        except MyException as e:
            return False
        
    def load_model(self,) -> Trained_Complete_Model:
        return self.s3.load_model(self.model_path, self.bucket_name)
    
    def save_model(self, from_file, remove:bool = False) -> None:
        try:
            print("from_file:", from_file)
            print("type:", type(from_file))
            self.s3.upload_file(from_file, self.model_path, self.bucket_name, remove)

        except Exception as e:
            raise MyException(e, sys)
        
    def predict(self, dataframe:DataFrame):
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe)
        except Exception as e:
            raise MyException(e, sys)