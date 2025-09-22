from dataclasses import dataclass
from hate_spech.constants import *
import os

@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.LOCAL_DATA_DIR: str = os.path.join(os.getcwd(), "data")  # Local data folder
        self.ZIP_FILE_NAME = ZIP_FILE_NAME

        self.DATA_INGESTION_ARTIFACTS_DIR: str = os.path.join(os.getcwd(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
        
        # Path to the extracted imbalanced CSV
        self.DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_IMBALANCE_DATA_DIR)
        
        # Path to the raw dataset CSV
        self.NEW_DATA_ARTIFACTS_DIR: str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_RAW_DATA_DIR)

        # Location to store the ZIP file (if copying locally)
        self.ZIP_FILE_DIR = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR)
        self.ZIP_FILE_PATH = os.path.join(self.LOCAL_DATA_DIR, self.ZIP_FILE_NAME)