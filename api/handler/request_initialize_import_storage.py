import traceback
from flask import current_app

from api.abstract_label_studio import AbstractLabelStudio
from api.entity.payload_initialize_import_storage import IInitializeImportStorage, PayloadInitializeImportStorage
from utility.request import Request


class RequestInitializeImportStorage(AbstractLabelStudio):
    def __init__(self, request_id: str, payload: IInitializeImportStorage):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- PAYLOAD: {self.payload}")

            
            query = f"SELECT * FROM label_project WHERE label_studio_internal_id = '{self.payload['label_studio_internal_id']}' AND project_title = '{self.payload['project_title']}' AND set_id = '{self.payload['set_id']}'"
            dao_request = Request()
            response = dao_request.query(self.request_id, query)
            if "response" in response and response["response"]["label_project_id"] != "":
                return {"status": "SUCCESS", "data": {"import_storage_id": response["response"]["import_storage_id"]}}



            response = self.create_import_storage(PayloadInitializeImportStorage.form_request_payload(self.payload))

            if "detail" in response:
                current_app.logger.error(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: {response['detail']}")
                raise Exception(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: {response['detail']}")
            
            if type(response["id"]) == int:
                update_response = dao_request.update(self.request_id, "label_project", "label_project_id", self.payload["label_project_id"], {"import_storage_id": response["id"]})
                if "response" not in update_response and update_response["response"] is not True:
                    current_app.logger.error(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- IMPORT_STORAGE_ID_NOT_SAVED_IN_DB --- STORAGE_ID:{response['id']} LABEL_PROJECT_ID: {self.payload['label_project_id']}")
                else:
                    current_app.logger.info(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- IMPORT_STORAGE_ID_SAVED_IN_DB --- STORAGE_ID:{response['id']} LABEL_PROJECT_ID: {self.payload['label_project_id']}")



            return {"status": "SUCCESS", "data": {"import_storage_id": response["id"]}}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- {traceback.format_exc()} -- ERROR: {str(e)}")
            return {"status": "FAILED", "error": str(e)}