import traceback
from flask import current_app, jsonify, make_response
from interface.abstract_handler import AbstractHandler
from utility.request import Request


class RequestGetLabelProjectsList(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- GET_LABEL_PROJECTS_LIST -- ARGS: {self.args}")

            dao_request = Request()
            label_project_list_response = dao_request.read_list(self.request_id, "label_project", self.args)

            if "response" not in label_project_list_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- GET_LABEL_PROJECTS_LIST -- ERROR: No response from DB")
                return {"status": "FAILED", "error": "No response from DB"}
            elif label_project_list_response["response"] == None:
                current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- GET_LABEL_PROJECTS_LIST -- INFO: No label projects found")
                return {"status": "SUCCESS", "data": []}
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- GET_LABEL_PROJECTS_LIST RESPONSE: {label_project_list_response['response']}")    
            response = make_response(jsonify({"status": "SUCCESS", "data": label_project_list_response["response"]}), 200)
            response.headers['Access-Control-Allow-Origin'] = "http://localhost:5173"
            response.headers['Access-Control-Allow-Credentials'] = "true"
            return response


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- {traceback.format_exc()} -- ERROR: {str(e)}")
            return {"status": "FAILED", "error": str(e)}
