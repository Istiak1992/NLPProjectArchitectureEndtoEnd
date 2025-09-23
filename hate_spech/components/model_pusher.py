import sys
import os
import shutil
from hate_spech.logger import logging
from hate_spech.exception import CustomException
from hate_spech.entity.config_entity import ModelPusherConfig
from hate_spech.entity.artifact_entity import ModelPusherArtifacts


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        """
        :param model_pusher_config: Configuration for model pusher
        """
        self.model_pusher_config = model_pusher_config

    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        """
        Method Name :   initiate_model_pusher
        Description :   This method copies the trained model 
                        from artifacts to the saved_models directory.

        Output      :   ModelPusherArtifacts with saved model path
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")
        try:
            os.makedirs(self.model_pusher_config.SAVED_MODEL_DIR, exist_ok=True)

            # Source: trained model path
            source_model_path = os.path.join(
                self.model_pusher_config.TRAINED_MODEL_DIR, 
                self.model_pusher_config.MODEL_NAME
            )

            # Destination: permanent saved_models path
            destination_model_path = self.model_pusher_config.SAVED_MODEL_PATH

            # Copy the model file
            shutil.copy(source_model_path, destination_model_path)

            logging.info(f"Model successfully copied to {destination_model_path}")

            # Create artifact object
            model_pusher_artifact = ModelPusherArtifacts(
                saved_model_path=destination_model_path
            )

            logging.info("Exited initiate_model_pusher method of ModelPusher class")
            return model_pusher_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
