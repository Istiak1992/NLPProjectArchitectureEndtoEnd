import os
import sys
import keras
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

from hate_spech.logger import logging
from hate_spech.exception import CustomException
from keras.utils import pad_sequences
from hate_spech.constants import *
from hate_spech.entity.config_entity import ModelEvaluationConfig
from hate_spech.entity.artifact_entity import (
    ModelEvaluationArtifacts,
    ModelTrainerArtifacts,
    DataTransformationArtifacts,
)


class ModelEvaluation:
    def __init__(
        self,
        model_evaluation_config: ModelEvaluationConfig,
        model_trainer_artifacts: ModelTrainerArtifacts,
        data_transformation_artifacts: DataTransformationArtifacts,
    ):
        """
        Local-only model evaluation (no GCloud).
        """
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts = data_transformation_artifacts

    def get_best_model_local(self) -> str:
        """
        Get best model path from local drive.
        :return: path to best model (if exists)
        """
        try:
            logging.info("Checking for best model in local storage")

            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH, exist_ok=True)

            best_model_path = os.path.join(
                self.model_evaluation_config.BEST_MODEL_DIR_PATH,
                self.model_evaluation_config.MODEL_NAME,
            )

            if os.path.isfile(best_model_path):
                logging.info(f"Best model found locally at {best_model_path}")
                return best_model_path
            else:
                logging.info("No best model found locally")
                return None

        except Exception as e:
            raise CustomException(e, sys) from e

    def evaluate(self, model_path: str) -> float:
        """
        Evaluate model against test dataset.
        :param model_path: Path to trained/best model
        :return: Accuracy
        """
        try:
            logging.info(f"Evaluating model from {model_path}")

            x_test = pd.read_csv(self.model_trainer_artifacts.x_test_path, index_col=0)
            y_test = pd.read_csv(self.model_trainer_artifacts.y_test_path, index_col=0)

            with open("tokenizer.pickle", "rb") as handle:
                tokenizer = pickle.load(handle)

            model = keras.models.load_model(model_path)

            x_test = x_test["tweet"].astype(str)
            x_test = x_test.squeeze()
            y_test = y_test.squeeze()

            test_sequences = tokenizer.texts_to_sequences(x_test)
            test_sequences_matrix = pad_sequences(test_sequences, maxlen=MAX_LEN)

            accuracy = model.evaluate(test_sequences_matrix, y_test, verbose=0)
            logging.info(f"Test accuracy: {accuracy}")

            # Confusion matrix for reference
            preds = model.predict(test_sequences_matrix)
            preds = (preds.flatten() >= 0.5).astype(int)
            cm = confusion_matrix(y_test, preds)
            logging.info(f"Confusion Matrix:\n{cm}")

            return accuracy[1] if isinstance(accuracy, (list, tuple)) else accuracy  # [loss, acc]
        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        """
        Compare trained model with best local model and decide acceptance.
        """
        logging.info("Initiating Model Evaluation")
        try:
            # Evaluate trained model
            trained_model_accuracy = self.evaluate(
                self.model_trainer_artifacts.trained_model_path
            )

            # Check for existing best model locally
            best_model_path = self.get_best_model_local()

            if not best_model_path:
                # No best model exists -> accept trained model
                is_model_accepted = True
                logging.info("No local best model found. Accepting trained model.")

            else:
                best_model_accuracy = self.evaluate(best_model_path)

                if trained_model_accuracy > best_model_accuracy:
                    is_model_accepted = True
                    logging.info("Trained model outperformed best model. Accepting trained model.")
                else:
                    is_model_accepted = False
                    logging.info("Best model is still better. Rejecting trained model.")

            return ModelEvaluationArtifacts(is_model_accepted=is_model_accepted)

        except Exception as e:
            raise CustomException(e, sys) from e
