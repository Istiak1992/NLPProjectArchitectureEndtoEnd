import os
import sys

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script [{0}] at line number [{1}] with error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):  # Inherit from built-in Exception
    def __init__(self, error_message, error_detail):
        """
        :param error_message: error message in string format
        :param error_detail: sys module (for traceback)
        """
        super().__init__(error_message)
        # Use the helper function here to get detailed error message
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message
