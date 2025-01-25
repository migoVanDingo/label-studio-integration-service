import json, requests
import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.Constant import Constant
from utility.payload.job_payload import JobPayload
from utility.request import Request


class WebhookHandler(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:

            if "project" not in self.payload or "id" not in self.payload["project"]:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Invalid webhook payload")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Invalid Webhook payload")
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- WEBHOOK_PAYLOAD: {self.payload}")


            description = json.loads(self.payload["project"]["description"])
            # Get label project from db
            dao_request = Request()
            label_project_response = dao_request.read(self.request_id, "label_project", {"label_studio_internal_id": self.payload["project"]["id"]})

            if "response" not in label_project_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Could not retrieve label project from DB")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Could not handle webhook update. Could not retrieve label project from DB")
            
            # Add dataset_directory_path to payload, this is where annotation files will be stored
            self.payload["dataset_directory_path"] = label_project_response["response"]["dataset_directory_path"]
            self.payload["label_project_id"] = label_project_response["response"]["label_project_id"]
            self.payload["set_name"] = label_project_response["response"]["set_name"]

            if "data" in self.payload["task"]:
                if "video" in self.payload["task"]["data"]:
                    video_string = self.payload["task"]["data"]["video"]
                    #Last element of the video string is the video name
                    file_name = video_string.split("/")[-1]
                    self.payload["file_name"] = file_name
                else:
                    current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Could not retrieve video name from task data")
                    raise Exception(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Could not handle webhook update. Could not retrieve video name from task data")


            # Form job payload and send to job-delegation-service
            payload = JobPayload.form_job_payload(self.payload, description)

            response = requests.post(Constant.base_url + Constant.services["JOB"]["PORT"] + Constant.services["JOB"]["ENDPOINT"]["CREATE-JOB"], json=payload)
            
            
            if response is None:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: No response from job-delegation-service")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Could not handle webhook update. No response from job-delegation-service")

            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- JOB_DELEGATION_RESPONSE: {response}")


            return {"status": "SUCCESS"}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} -- ERROR: {str(e)}")
            return {"status": "FAILED", "error": str(e)}
        


       