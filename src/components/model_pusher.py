import sys
from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.s3_estimator import Cloud_Saved_Model

class ModelPusher:
    def __init__(self, model_evaluation_artifact : ModelEvaluationArtifact, model_pusher_config : ModelPusherConfig):

        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.cloud_model = Cloud_Saved_Model(model_pusher_config.bucket_name, model_pusher_config.s3_model_key_path)


    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logging.info("Initiating Model Pusher method!!!")
            
            self.cloud_model.save_model(self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(self.model_pusher_config.bucket_name, self.model_pusher_config.s3_model_key_path)

            logging.info("Exited Initiate Model Pusher method!!!")

            return model_pusher_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        