import sys
from typing import Tuple

import pandas as pd
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.exception import MyException
from src.logger import logging
from src.utils import load_object, save_object
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact

from src.entity.estimator import Trained_Complete_Model

class ModelTrainer:
    def __init__(self, data_transformation_artifact : DataTransformationArtifact, model_trainer_config : ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train : pd.DataFrame, test : pd.DataFrame) -> Tuple[object, object]:

        try:
            logging.info("Training Support Vector Classifier with Specified Parameter!!!")

            X_train, y_train, X_test, y_test = train.iloc[:, 1:], train.iloc[:, 0].astype(int), test.iloc[:, 1:], test.iloc[:, 0].astype(int)

            model = LinearSVC(class_weight="balanced", C=self.model_trainer_config.clf__C, random_state=self.model_trainer_config._random_state)

            logging.info("Fitting the Model...")
            model.fit(X_train, y_train)

            logging.info("Prediction and Evaluation...")
            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)

            metric_artifact = ClassificationMetricArtifact(f1, precision, recall)

            return model, metric_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:

        try: 
            logging.info("Initiating the Model Trainer!!!")

            train_arr = pd.read_csv(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = pd.read_csv(self.data_transformation_artifact.transformed_test_file_path)

            trained_model, metric_artifact = self.get_model_object_and_report(train_arr, test_arr)

            preprocessing_obj = load_object(self.data_transformation_artifact.transformed_object_file_path)

            if accuracy_score(train_arr.iloc[:, 0].astype(int), trained_model.predict(train_arr.iloc[:, 1:])) < self.model_trainer_config.expected_accuracy:
                logging.info("Model's accuracy not above the base expected accuracy!!!")
                raise Exception("Model's accuracy not above the base expected accuracy!!!")
            

            logging.info("Saving new model as performance is better than previous one...")
            
            complete_model = Trained_Complete_Model(preprocessing_obj, trained_model)

            save_object(self.model_trainer_config.trained_model_file_path, complete_model)

            model_trainer_artifact = ModelTrainerArtifact(self.model_trainer_config.trained_model_file_path, metric_artifact)

            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")

            return model_trainer_artifact
        
        except Exception as e:
            raise MyException(e, sys)