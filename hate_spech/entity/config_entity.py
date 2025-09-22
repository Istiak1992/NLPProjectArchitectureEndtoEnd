from dataclasses import dataclass
from hate_spech.constants import *
import os

@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.LOCAL_DATA_DIR: str = os.path.join(os.getcwd(), "data")  # Local data folder
        self.ZIP_FILE_NAME = ZIP_FILE_NAME

        # Base artifacts folder
        self.DATA_INGESTION_ARTIFACTS_DIR: str = os.path.join(
            os.getcwd(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR
        )

        #  Add "data" subfolder here
        self.DATA_INGESTION_DATA_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, "data")

        # Path to the extracted imbalanced CSV
        self.DATA_ARTIFACTS_DIR: str = os.path.join(
            self.DATA_INGESTION_DATA_DIR, DATA_INGESTION_IMBALANCE_DATA_DIR
        )

        # Path to the raw dataset CSV
        self.NEW_DATA_ARTIFACTS_DIR: str = os.path.join(
            self.DATA_INGESTION_DATA_DIR, DATA_INGESTION_RAW_DATA_DIR
        )

        # Location to store the ZIP file (if copying locally)
        self.ZIP_FILE_DIR = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR)
        self.ZIP_FILE_PATH = os.path.join(self.LOCAL_DATA_DIR, self.ZIP_FILE_NAME)



@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.DATA_TRANSFORMATION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(),ARTIFACTS_DIR,DATA_TRANSFORMATION_ARTIFACTS_DIR)
        self.TRANSFORMED_FILE_PATH = os.path.join(self.DATA_TRANSFORMATION_ARTIFACTS_DIR,TRANSFORMED_FILE_NAME)
        self.ID = ID
        self.AXIS = AXIS
        self.INPLACE = INPLACE 
        self.DROP_COLUMNS = DROP_COLUMNS
        self.CLASS = CLASS 
        self.LABEL = LABEL
        self.TWEET = TWEET