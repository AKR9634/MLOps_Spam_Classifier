import sys
from src.entity.config_entity import SpamClassifierConfig
from src.entity.s3_estimator import Cloud_Saved_Model
from src.exception import MyException
from src.logger import logging
from pandas import DataFrame



class SpamData:
    def __init__(self, message):

        try:
            self.message = message
        except Exception as e:
            raise MyException(e, sys)
    
    def get_spam_data_as_dict(self):

        try:
            input_data = {"message" : [self.message]}
            return input_data
        except Exception as e:
            raise MyException(e, sys)
        
    def get_spam_input_data_frame(self) -> DataFrame:
        try:
            spam_data_input = self.get_spam_data_as_dict()
            return DataFrame(spam_data_input)
        except Exception as e:
            raise MyException(e, sys)
        

class SpamDataClassifier:
    def __init__(self, prediction_pipeline_config: SpamClassifierConfig = SpamClassifierConfig(), ) -> None:
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise MyException(e, sys)
        
    def predict(self, dataframe) -> str:
        try:
            model = Cloud_Saved_Model(self.prediction_pipeline_config.model_bucket_name, self.prediction_pipeline_config.model_file_path)
            result = model.predict(dataframe)

            return result
        except Exception as e:
            raise MyException(e, sys)