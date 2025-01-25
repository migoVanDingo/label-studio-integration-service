import os
import subprocess
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.Constant import Constant


class RequestPullAnnotationAllFrames(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- PULL_ANNOTATION_ALL_FRAMES -- PAYLOAD: {self.payload}")

            path = self.payload["temp_output_path"]
            data_file = self.payload["file_name"]
            file_name = data_file.split(".")[0] + ".json"

            command = self._form_pull_command(self.payload["project_id"], self.payload["task_id"], Constant.label_studio_user_token, file_name)

            os.chdir(path)
            subprocess.run(command, shell=True, check=True)


            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- PULL_ANNOTATION_ALL_FRAMES -- temp_output_path: {path} -- file_name: {file_name}")


            return {"status": "SUCCESS", "data": {"temp_output_path": path, "json_file_name": file_name}}

        except Exception as e:
            return {"status": "FAILED", "error": str(e)}
        
    def _form_pull_command(self, project_id, task_id, token, file_name):
        return f"curl -X GET 'http://localhost:8080/api/projects/{str(project_id)}/export?exportType=JSON&interpolate_key_frames=true&ids[]={str(task_id)}' -H 'Authorization: Token {token}' --output {file_name}"