import os
import sys
from zipfile import ZipFile
from hate_spech.logger import logging
from hate_spech.exception import CustomException
from hate_spech.entity.config_entity import DataIngestionConfig
from hate_spech.entity.artifact_entity import DataIngestionArtifacts


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config

    def get_data_from_local(self) -> None:
        """
        Verifies that the local ZIP file exists and creates the artifact directory.
        """
        try:
            logging.info("Entered the get_data_from_local method of DataIngestion class")

            # Ensure the artifacts directory exists
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            # Check if the ZIP file exists
            if not os.path.exists(self.data_ingestion_config.ZIP_FILE_PATH):
                raise FileNotFoundError(f"ZIP file not found at: {self.data_ingestion_config.ZIP_FILE_PATH}")

            logging.info(f"Found ZIP file at: {self.data_ingestion_config.ZIP_FILE_PATH}")
            logging.info("Exited the get_data_from_local method of DataIngestion class")

        except Exception as e:
            raise CustomException(e, sys) from e

    def unzip_and_clean(self):
        """
        Unzips the local dataset file into the designated directory.
        """
        logging.info("Entered the unzip_and_clean method of DataIngestion class")
        try:
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)

            logging.info("Unzipping completed successfully.")
            logging.info("Exited the unzip_and_clean method of DataIngestion class")

            return (
                self.data_ingestion_config.DATA_ARTIFACTS_DIR,
                self.data_ingestion_config.NEW_DATA_ARTIFACTS_DIR
            )

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        """
        Main method to perform the ingestion from local ZIP and return artifact paths.
        """
        logging.info("Entered the initiate_data_ingestion method of DataIngestion class")

        try:
            self.get_data_from_local()
            logging.info("Local ZIP file verified.")

            imbalance_data_file_path, raw_data_file_path = self.unzip_and_clean()
            logging.info("Data unzipped and ready for use.")

            data_ingestion_artifacts = DataIngestionArtifacts(
                imbalance_data_file_path=imbalance_data_file_path,
                raw_data_file_path=raw_data_file_path
            )

            logging.info(f"Data ingestion artifacts created: {data_ingestion_artifacts}")
            logging.info("Exited the initiate_data_ingestion method of DataIngestion class")

            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
