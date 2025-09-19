from hate_spech.logger import logging
from hate_spech.exception import CustomException
import sys

try:
    a = 7 / "0"
except Exception as e:
    raise CustomException(e, sys) from e
