import os
import sys
import keras
import pickle
from keras.utils import pad_sequences
from hate_spech.logger import logging
from hate_spech.constants import MODEL_NAME
from hate_spech.exception import CustomException
from hate_spech.components.data_transformation import DataTransformation
from hate_spech.entity.config_entity import DataTransformationConfig
from hate_spech.entity.artifact_entity import DataIngestionArtifacts


class PredictionPipeline:
    def __init__(self,
                 model_dir: str = "artifacts/PredictModel",
                 tokenizer_path: str = "artifacts/tokenizer/tokenizer.pickle",
                 imbalance_data_path: str = "artifacts/data/imbalance_data.csv",
                 raw_data_path: str = "artifacts/data/raw_data.csv"):
        """
        Initializes the PredictionPipeline for local drive usage.
        """
        try:
            # Paths
            self.model_dir = model_dir
            self.model_name = MODEL_NAME
            self.model_path = os.path.join(self.model_dir, self.model_name)
            os.makedirs(self.model_dir, exist_ok=True)

            self.tokenizer_path = tokenizer_path
            if not os.path.exists(os.path.dirname(self.tokenizer_path)):
                os.makedirs(os.path.dirname(self.tokenizer_path), exist_ok=True)

            # Data artifacts
            self.data_ingestion_artifacts = DataIngestionArtifacts(
                imbalance_data_file_path=imbalance_data_path,
                raw_data_file_path=raw_data_path
            )

            # Data transformation
            self.data_transformation = DataTransformation(
                data_transformation_config=DataTransformationConfig(),
                data_ingestion_artifacts=self.data_ingestion_artifacts
            )

        except Exception as e:
            raise CustomException(e, sys) from e

    def get_model_from_local(self) -> str:
        """
        Returns the local model path if exists.
        """
        try:
            logging.info(f"Looking for model at: {self.model_path}")
            if not os.path.exists(self.model_path):
                logging.error(f"Model file not found at {self.model_path}")
                raise FileNotFoundError(f"Model file not found at {self.model_path}")
            logging.info(f"Model found at {self.model_path}")
            return self.model_path
        except Exception as e:
            raise CustomException(e, sys) from e

    def load_tokenizer(self):
        """
        Load tokenizer from local path.
        """
        try:
            if not os.path.exists(self.tokenizer_path):
                logging.error(f"Tokenizer file not found at {self.tokenizer_path}")
                raise FileNotFoundError(f"Tokenizer file not found at {self.tokenizer_path}")

            with open(self.tokenizer_path, 'rb') as handle:
                tokenizer = pickle.load(handle)
            logging.info("Tokenizer loaded successfully")
            return tokenizer
        except Exception as e:
            raise CustomException(e, sys) from e

    def predict(self, text: str) -> str:
        """
        Predict if text is 'hate and abusive' or 'no hate'.
        """
        try:
            model_path = self.get_model_from_local()
            model = keras.models.load_model(model_path)
            tokenizer = self.load_tokenizer()

            # Preprocess text
            cleaned_text = self.data_transformation.concat_data_cleaning(text)
            seq = tokenizer.texts_to_sequences([cleaned_text])
            padded = pad_sequences(seq, maxlen=300)

            # Prediction
            pred = model.predict(padded)
            logging.info(f"Prediction raw output: {pred}")

            return "hate and abusive" if pred[0][0] > 0.5 else "no hate"

        except Exception as e:
            raise CustomException(e, sys) from e

    def run_pipeline(self, text: str) -> str:
        """
        Runs the full pipeline: load model + tokenizer + predict.
        """
        try:
            logging.info("Running full prediction pipeline")
            result = self.predict(text)
            logging.info("Prediction pipeline completed successfully")
            return result
        except Exception as e:
            raise CustomException(e, sys) from e
