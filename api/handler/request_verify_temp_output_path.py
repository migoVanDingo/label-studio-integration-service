import os

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.Constant import Constant


class RequestVerifyTempOutputPath(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- VERIFY_TEMP_OUTPUT_PATH")
            
            temp_output_path = os.path.join(Constant.labeler_output_dir, self.payload["dataset_id"])

            if not os.path.exists(temp_output_path):
                os.makedirs(temp_output_path)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- TEMP_OUTPUT_PATH: {temp_output_path}")

            return {"status": "SUCCESS", "data": {"temp_output_path": temp_output_path}}

        except Exception as e:
            return {"status": "FAILED", "error": str(e)}