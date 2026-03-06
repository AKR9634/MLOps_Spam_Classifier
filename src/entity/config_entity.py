import os
from dataclasses import dataclass
from datetime import datetime


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
artifact_dir = os.path.join("artifact", TIMESTAMP)

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(artifact_dir, "data_ingestion")
    feature_store_file_path: str = os.path.join(data_ingestion_dir, "feature_store\data.csv")
    training_file_path: str = os.path.join(data_ingestion_dir, "ingested\\train.csv")
    test_file_path: str = os.path.join(data_ingestion_dir, "ingested\\test.csv")
    train_test_split_ratio: float = 0.25
    collection_name: str = "Spam_Data"

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(artifact_dir, "data_validation")
    validation_report_file_path: str = os.path.join(data_validation_dir, "report.yaml")

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(artifact_dir, "data_transformation")
    transformed_train_file_path: str = os.path.join(data_transformation_dir, "transformed", "train.csv")
    tranformed_test_file_path: str = os.path.join(data_transformation_dir, "transformed", "test.csv")
    transformed_object_file_path: str = os.path.join(data_transformation_dir, "tranformed_object", "preprocessing_model.pkl")

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(artifact_dir, "model_trainer")
    trained_model_file_path: str = os.path.join(model_trainer_dir, "trained_model/model.pkl")
    expected_accuracy: float = 0.6
    clf__C = 10
    _random_state = 43
    tfidf__ngram_range = (1, 2)

@dataclass
class ModelEvaluationConfig:
    changed_threshold_score: float = 0.02
    bucket_name: str =  ""
    s3_model_key_path: str= "model.pkl"

@dataclass
class ModelPusherConfig:
    bucket_name : str = ""
    s3_model_key_path : str = "model.pkl"