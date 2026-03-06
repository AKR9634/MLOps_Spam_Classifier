from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelTrainerArtifact, DataIngestionArtifact, ModelEvaluationArtifact
from sklearn.metrics import f1_score
from src.exception import MyException
from src.logger import logging
from src.utils import load_object
import sys
import pandas as pd
from typing import Optional
from src.entity.s3_estimator import Cloud_Saved_Model
from dataclasses import dataclass

@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:

    def __init__(self, model_eval_config: ModelEvaluationConfig, data_ingestion_artifact: DataIngestionArtifact, model_trainer_artifact: ModelTrainerArtifact):

        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MyException(e, sys)
        
    
    def get_best_model(self) -> Optional[Cloud_Saved_Model]:

        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key_path
            cloud_model = Cloud_Saved_Model(bucket_name, model_path)

            if cloud_model.is_model_present(model_path):
                return cloud_model
            return None
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
    

    def evaluate_model(self) -> EvaluateModelResponse:

        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            x, y = test_df.iloc[:, 1:], test_df.iloc[:, 0]

            x = self._drop_columns(x)
            x = self._rename_columns(x)

            y = y.map({"ham":0, "spam":1})
            trained_model = load_object(self.model_trainer_artifact.trained_model_file_path)
            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score

            best_model_f1_score = None
            best_model = self.get_best_model()
            if best_model is not None:
                y_hat_best_model = best_model.predict(x)
                best_model_f1_score = f1_score(y, y_hat_best_model)

            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score
            result = EvaluateModelResponse(trained_model_f1_score, best_model_f1_score, trained_model_f1_score > tmp_best_model_score, trained_model_f1_score - tmp_best_model_score)

            logging.info(f"Result: {result}")
            return result
        
        except Exception as e:
            raise MyException(e, sys)
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:

        try:
            logging.info("Initialized Model Evaluation Component!!!")
            evaluate_model_response = self.evaluate_model()
            s3_model_path = self.model_eval_config.s3_model_key_path

            model_evaluation_artifact = ModelEvaluationArtifact(evaluate_model_response.is_model_accepted, s3_model_path, self.model_trainer_artifact.trained_model_file_path, evaluate_model_response.difference)

            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e, sys)