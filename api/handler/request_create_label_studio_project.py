import os
import traceback

from flask import current_app, json
import requests
from dotenv import load_dotenv
load_dotenv("/Users/bubz/Developer/master-project/label-studio-integration-service/.env")
from api.abstract_label_studio import AbstractLabelStudio
from api.entity.interface_create_label_studio_project import ICreateLabelStudioProject
from dao.table_label_studio_project import TableLabelStudioProject


class RequestCreateLabelStudioProject(AbstractLabelStudio):
    def __init__(self, payload):
        super().__init__()
        self.payload = payload
        self.table_label_studio_project = TableLabelStudioProject()

    def do_process(self):
        try:
            current_app.logger.info(f"CLASS: {self.__class__.__name__} -- PAYLOAD: {self.payload}")

            label_studio_payload = {
                "title": self.payload["name"],
                "description": self.payload["description"]
            }

            response = self.create_label_studio_project(json.dumps(label_studio_payload))

            #current_app.logger.info(f"CLASS: {self.__class__.__name__} -- RESPONSE: {response}")


            if "status_code" in response:
                return { "status": "failed", "error": response['detail'] }

            insert_payload = {
                "label_studio_project_id": response["id"],
                "datastore_subset_id": self.payload["datastore_subset_id"],
                "name": self.payload["name"],
                "description": self.payload["description"],
                "created_by": self.payload["created_by"],
                "result": json.dumps(response)
            }
            validated_payload = ICreateLabelStudioProject(**insert_payload)
            
            #current_app.logger.info(f"CLASS: {self.__class__.__name__} -- LABEL_STUDIO_PROJECT INSERT: {validated_payload}")

            record = self.table_label_studio_project.insert(validated_payload.model_dump())

            return_object = { "status": "success", "data": record }

            current_app.logger.info(f"CLASS: {self.__class__.__name__} -- RETURN: {return_object}")
            
            return return_object
        
        except Exception as e:
            current_app.logger.error(f"CLASS: {self.__class__.__name__} -- ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return { "status": "failed", "error": str(e) }
        

