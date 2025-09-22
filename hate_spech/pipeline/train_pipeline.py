import sys
from hate_spech.logger import logging
from hate_spech.exception import CustomException
from hate_spech.components.data_ingestion import DataIngestion
#from hate_spech.components.data_transforamation import DataTransformation
#from hate_spech.components.model_trainer import ModelTrainer
#from hate_spech.components.model_evaluation import ModelEvaluation
#from hate_spech.components.model_pusher import ModelPusher

#from hate_spech.entity.config_entity import (DataIngestionConfig,DataTransformationConfig, ModelTrainerConfig,ModelEvaluationConfig, ModelPusherConfig)
from hate_spech.entity.config_entity import  DataIngestionConfig
#from hate_spech.entity.artifact_entity import (DataIngestionArtifacts, DataTransformationArtifacts,ModelTrainerArtifacts, ModelEvaluationArtifacts,ModelPusherArtifacts)
from hate_spech.entity.artifact_entity import DataIngestionArtifacts

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from local drive")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train and valid data from local drive")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e

    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of Trainpipeline class")
        try:
            data_ingestion_artifacts = self.start_data_ingestion()

            logging.info("Entered the run_pipeline method of Trainpipeline class")

        except Exception as e:
            raise CustomException(e, sys) from e

   