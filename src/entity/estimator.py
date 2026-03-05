import sys
import pandas as pd
from pandas import DataFrame

from sklearn.pipeline import Pipeline
from src.exception import MyException
from src.logger import logging

class Trained_Complete_Model:
    def __init__(self, preprocessing_object : Pipeline, training_model_object : object):

        self.preprocessing_object = preprocessing_object
        self.training_model_object = training_model_object

    def predict(self, dataframe: pd.DataFrame) -> DataFrame:

        try:
            logging.info("Starting Prediction Process!!!")

            transformed_feature = self.preprocessing_object.transform(dataframe)
            predictions = self.training_model_object.predict(transformed_feature)

            logging.info("Predicted using the trained model!!!")

            return predictions
        
        except Exception as e:
            raise MyException(e, sys)
        
    def __repr__(self):
        return f"{type(self.training_model_object).__name__}()"
    
    def __str__(self):
        return f"{type(self.training_model_object).__name__}()"