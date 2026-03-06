import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

from src.entity.config_entity import DataIngestionConfig
from src.entity.config_entity import DataValidationConfig
from src.entity.config_entity import DataTransformationConfig
from src.entity.config_entity import ModelTrainerConfig
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.config_entity import ModelPusherConfig


from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.artifact_entity import DataValidationArtifact
from src.entity.artifact_entity import DataTransformationArtifact
from src.entity.artifact_entity import ModelTrainerArtifact
from src.entity.artifact_entity import ModelEvaluationArtifact
from src.entity.artifact_entity import ModelPusherArtifact


class TrainingPipeline:

    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        self.model_pusher_config = ModelPusherConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:
            logging.info("Starting Data Ingestion!!!")
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Completed Data Ingestion!!!")

            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact : DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("Starting Data Validation!!!")
            data_validation = DataValidation(data_ingestion_artifact, self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Completed Data Validation!!!")

            return data_validation_artifact
        
        except Exception as e:
            raise MyException(e, sys)
    
    def start_data_transformation(self, data_ingestion_artifact : DataIngestionArtifact, data_validation_artifact: DataValidationArtifact):
        try:
            logging.info("Starting Data Tranformation!!!")
            data_transformation = DataTransformation(data_ingestion_artifact, data_validation_artifact, self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()

            logging.info("Completed Data Transformation!!!")

            return data_transformation_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            logging.info("Starting Model Training!!!")
            model_trainer = ModelTrainer(data_transformation_artifact, self.model_trainer_config)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            
            logging.info("Completed Model Training!!!")

            return model_trainer_artifact
        
        except Exception as e:
            raise MyException(e, sys)


    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               model_trainer_artifact: ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            logging.info("Starting Model Evaluation!!!")
            model_evaluation = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            logging.info("Completed Model Evaluation!!!")
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e, sys)

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
       
        try:
            logging.info("Starting Model Pusher!!!")
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                       model_pusher_config=self.model_pusher_config
                                       )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            logging.info("Completed Model Pusher!!!")
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e, sys)


    def run_pipeline(self, ) -> None:
        
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact, data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact)
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact, model_trainer_artifact)
            
            if not model_evaluation_artifact.is_model_accepted:
                logging.info("Model not accepted!!!")
                return None
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact)

        except Exception as e:
            raise MyException(e, sys)