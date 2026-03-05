import json
import sys
import os
import pandas as pd

from src.exception import MyException
from src.logger import logging
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.utils import read_yaml_file, write_yaml_file

SCHEMA_PATH_FILE = "config/schema.yaml"


class DataValidation:

    def __init__(self, data_ingestion_artifact : DataIngestionArtifact, data_validation_config : DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_PATH_FILE)

        except Exception as e:
            raise MyException(e, sys)
        

    def validate_number_of_columns(self, dataframe : pd.DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            return status
        except Exception as e:
            raise MyException(e, sys)
        
    
    def does_columns_matches(self, df: pd.DataFrame) -> bool:
        try:
            dataframe_columns = df.columns

            for column in self._schema_config["columns"]:
                if column not in dataframe_columns:
                    return False
                
            return True
        except Exception as e:
            raise MyException(e, sys)


    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)   
        
    
    def initiate_data_validation(self) -> DataValidationArtifact:

        try:
            validation_error_msg = ""
            logging.info("Initiating Data Validation process!!!")
            train_df, test_df = (DataValidation.read_data(self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(self.data_ingestion_artifact.test_file_path))

            status = self.validate_number_of_columns(train_df) and self.does_columns_matches(train_df)
            if not status:
                validation_error_msg += "Columns are missing in training dataframe!!!"
            

            status = self.validate_number_of_columns(test_df) and self.does_columns_matches(test_df)
            if not status:
                validation_error_msg += "Columns are missing in testing dataframe!!!"

            validation_status = len(validation_error_msg) == 0

            data_validation_artifact = DataValidationArtifact(
                validation_status = validation_status,
                message = validation_error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )



            os.makedirs(os.path.dirname(self.data_validation_config.validation_report_file_path), exist_ok=True)

            validation_report = {
                "validation_status" : validation_status,
                "message" : validation_error_msg.strip()
            }

            with open(self.data_validation_config.validation_report_file_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4)

            logging.info("Data Validation Completed and Data validation artifact created!!!")

            return data_validation_artifact
        
        except Exception as e:
            raise MyException(e, sys)