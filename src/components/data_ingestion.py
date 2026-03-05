import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.exception import MyException
from src.logger import logging
from src.data_access.mongoDB_data_access import MongoDB_Data_Access
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e, sys)
        
    
    def export_data_into_feature_store(self) -> DataFrame:

        try:
            logging.info("Exporting data from mongoDB!!!")
            my_data = MongoDB_Data_Access()
            df = my_data.export_collection_as_dataframe(self.data_ingestion_config.collection_name)
            os.makedirs(os.path.dirname(self.data_ingestion_config.feature_store_file_path), exist_ok=True)
            df.to_csv(self.data_ingestion_config.feature_store_file_path, index=False, header=True)

            return df
        
        except Exception as e:
            MyException(e, sys)


    
    def split_data_train_test(self, dataframe: DataFrame) -> None:
        try:
            logging.info("Performing train_test_split!!!")

            train, test = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_ingestion_config.test_file_path), exist_ok=True)

            train.to_csv(self.data_ingestion_config.training_file_path, index = False, header = True)
            test.to_csv(self.data_ingestion_config.test_file_path, index = False, header = True)

        except Exception as e:
            raise MyException(e, sys) 



    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        logging.info("Initiating Data Ingestion process!!!")

        try:
            dataframe = self.export_data_into_feature_store()
            self.split_data_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(self.data_ingestion_config.training_file_path, self.data_ingestion_config.test_file_path)
            logging.info("Data Ingestion Completed and Data Ingestion Artifact created successfully!!!")

            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys)