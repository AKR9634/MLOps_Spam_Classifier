import sys
import os
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from src.exception import MyException
from src.logger import logging
from src.utils import save_object, read_yaml_file


SCHEMA_PATH_FILE = "config/schema.yaml"


class DataTransformation:

    def __init__(self, data_ingestion_artifact : DataIngestionArtifact, data_validation_artifact : DataValidationArtifact, data_transformation_config : DataTransformationConfig):     
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(SCHEMA_PATH_FILE)

        except Exception as e:
            raise MyException(e, sys)
        
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)


    def _drop_columns(self, df):
        drop_col = self._schema_config["drop_columns"]
        for col in drop_col:
            if col in df.columns:
                df = df.drop(col, axis=1)
        return df
    
    def _rename_columns(self, df):
        column_rename = self._schema_config["rename_columns"]
        df = df.rename(columns = column_rename)

        return df
    
    @staticmethod
    def map_label(label_series):
        return label_series.map({"ham": 0, "spam": 1}).to_frame()
    
    @staticmethod
    def clean_series(text_series):
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))

        def clean_text(text):
            text = text.lower()
            text = re.sub(r'\d+', '', text)
            text = text.translate(str.maketrans('', '', string.punctuation))
            tokens = text.split()
            tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
            return " ".join(tokens)
        
        return text_series.apply(clean_text)
    
    def get_data_transformer_object(self) -> Pipeline:
        
        nltk.download('stopwords')
        nltk.download('wordnet')
       
        text_pipeline = Pipeline([
            ("clean_text", FunctionTransformer(self.clean_series)),
            ("tfidf", TfidfVectorizer(max_features=5000))
        ])

        column_transformer = ColumnTransformer(
            transformers=[
                ("text_processing", text_pipeline, "message")
            ]
        )

        pipeline = Pipeline([
            ("preprocessing", column_transformer)
        ])

        return pipeline


    def initiate_data_transformation(self) -> DataTransformationArtifact:

        try:
            logging.info("Initiating Data Tranfomation!!!")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            train_df = self._drop_columns(train_df)
            train_df = self._rename_columns(train_df)

            test_df = self._drop_columns(test_df)
            test_df = self._rename_columns(test_df)

            train_df["label"] = train_df["label"].map({"ham":0, "spam":1})
            test_df["label"] = test_df["label"].map({"ham":0, "spam":1})

            processor = self.get_data_transformer_object()

            X_train = train_df[["message"]]
            y_train = train_df["label"]

            X_test = test_df[["message"]]
            y_test = test_df["label"]

            processed_X_train = processor.fit_transform(X_train)
            processed_X_test = processor.transform(X_test)

            train_final = np.c_[y_train.values, processed_X_train.toarray()]
            test_final = np.c_[y_test.values, processed_X_test.toarray()]

            # smt = SMOTEENN(sampling_strategy="minority")
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_object_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_transformation_config.transformed_train_file_path), exist_ok=True)


            save_object(self.data_transformation_config.transformed_object_file_path, processor)

            pd.DataFrame(train_final).to_csv(self.data_transformation_config.transformed_train_file_path, index=False)
            pd.DataFrame(test_final).to_csv(self.data_transformation_config.tranformed_test_file_path, index=False)

            logging.info("Data Transformation Done!!!")

            return DataTransformationArtifact(self.data_transformation_config.transformed_object_file_path,
                                              self.data_transformation_config.transformed_train_file_path,
                                              self.data_transformation_config.tranformed_test_file_path)
        except Exception as e:
            raise MyException(e, sys)
