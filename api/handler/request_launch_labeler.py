import traceback
import webbrowser
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.Constant import Constant
from utility.request import Request



class RequestLaunchLabeler(AbstractHandler):
    def __init__(self, request_id: str, project_id: str):
        self.request_id = request_id
        self.project_id = project_id

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- LAUNCH_LABELER -- PROJECT_ID: {self.project_id}")

            dao_request = Request()
            label_project_response = dao_request.read(self.request_id, "label_project", {"label_project_id": self.project_id})

            if "response" not in label_project_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- LAUNCH_LABELER -- ERROR: No response from DB")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Failed to open labeling project, No response from DB")
            elif label_project_response["response"] == None:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- LAUNCH_LABELER -- ERROR: No project found")
                raise Exception(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: Failed to open labeling project, No project found")
            

            webbrowser.open(Constant.base_url + Constant.label_port + "/projects/" + str(label_project_response["response"]["label_studio_internal_id"]) + "/data")

            return {"status": "SUCCESS"}


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- {traceback.format_exc()} -- ERROR: {str(e)}")
            return {"status": "FAILED", "error": str(e)}
