from api.abstract_label_studio import AbstractLabelStudio
import traceback

from flask import current_app, json
from dotenv import load_dotenv

from api.entity.payload_create_label_studio_project import ICreateLabelProject, PayloadCreateLabelStudioProject
from utility.request import Request
load_dotenv(
    "/Users/bubz/Developer/master-project/label-studio-integration-service/.env")

"""
    Class RequestCreateLabelStudioProject:
    - This class is responsible for creating a Label Studio project
    - The Label Studio project is where the label config, instructions and project metadata are defined
    - Used in job-flow, or as standalone request handler.

    Super: AbstractLabelStudio
    - The abstract class which contains the abstracted Label Studio methods
    - These methods will form the payloads/headers/urls etc for interacting with the LabelStudio API

    Payload:
    class ICreateLabelProject(BaseModel):
        set_name: str
        project_name: str
        label_config: str
        datastore_id: str
        description: str
        config_order: list
        instructions: Optional[str]

    Return:
    class ReturnCreateLabelStudioProject:
        label_studio_internal_id: str (Generated by Label Studio)
        label_project_id: str (Generated by DB insert)
"""


class RequestCreateLabelStudioProject(AbstractLabelStudio):
    def __init__(self, request_id: str, payload: ICreateLabelProject):
        super().__init__()
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(
                f"{self.request_id} --- {self.__class__.__name__} -- CREATE_LABEL_PROJECT PAYLOAD: {self.payload}")
            
            dao_request = Request()

            
            label_project_response = dao_request.read(self.request_id, "label_project", { "set_id": self.payload["set_id"], "dataset_id": self.payload["dataset_id"], "project_name": self.payload["project_name"]})
            if "response" in label_project_response and label_project_response["response"] != None:
                current_app.logger.info(
                        f"{self.request_id} --- {self.__class__.__name__} -- LABEL_PROJECT_EXISTS: {label_project_response['response']}")
                return {"status": "SUCCESS", "data": {}}

            # Use payload to form Label Studio project title and description
            title = f"{self.payload['set_name']}__{self.payload['project_name']}"

            # -> Description: [{config field_name}: { payload[field_name]}] + description
            ## All of this data must be added to the label studio project description so that when the project is updated in Label Studio (e.g. people annotate video files) the files can then be identified and processed by the web app.
            description = {
                "description": self.payload["description"],
                "set_id": self.payload["set_id"],
                "dataset_id": self.payload["dataset_id"],
                "datastore_id": self.payload["datastore_id"],
                "project_name": self.payload["project_name"],
                "user_id": self.payload["user_id"],
                "tags": [{item["field_name"]: self.payload[item["field_name"]]}
                         for item in sorted(self.payload["config_order"], key=lambda item: item["order_index"])],

            }

            # Form payload for LabelStudio API
            label_studio_payload = PayloadCreateLabelStudioProject.form_label_studio_project_payload(title, json.dumps(
                description), self.payload["label_config"], self.payload["instructions"] if "instructions" in self.payload else "")

            current_app.logger.info(
                f"{self.request_id} --- {self.__class__.__name__} -- LABEL_STUDIO_PAYLOAD: {label_studio_payload}")

            # Create the label project in LabelStudio via API
            response = self.create_label_studio_project(
                json.dumps(label_studio_payload))

            current_app.logger.info(
                f"{self.request_id} --- {self.__class__.__name__} -- LABEL_STUDIO_RESPONSE: {response}")

            if "status_code" in response and response.status_code != 201:
                current_app.logger.error(
                    f"{self.request_id} --- {self.__class__.__name__} -- ERROR: {response['detail']}")
                raise Exception(
                    f"{self.request_id} --- {self.__class__.__name__} -- ERROR: LABEL_PROJECT_CREATION_FAILED --- {response['detail']}")

            label_studio_internal_id = response["id"]

            if "fps" in self.payload:
                fps = {"fps": self.payload["fps"]}
                description.update(fps)

            if "data_type" in self.payload:
                data_type = {"data_type": self.payload["data_type"]}
                description.update(data_type)

            metadata = {}

            metadata.update(description)

            # Insert the Label Studio project into the database
            insert_payload = PayloadCreateLabelStudioProject.form_insert_payload({
                "label_studio_internal_id": label_studio_internal_id,
                "label_studio_project_name": title,
                "set_id": self.payload["set_id"],
                "datastore_id": self.payload["datastore_id"],
                "set_name": self.payload["set_name"],
                "project_name": self.payload["project_name"],
                "metadata": json.dumps(metadata),
                "label_config": self.payload["label_config"],
                "dataset_directory_path": self.payload["dataset_directory_path"],
                "user_id": self.payload["user_id"],
                "dataset_id": self.payload["dataset_id"]
            })
            
            insert_response = dao_request.insert(self.request_id, "label_project", insert_payload)

            current_app.logger.error(
                    f"{self.request_id} --- {self.__class__.__name__} -- INSERT RESPONSE: {insert_response}")
            if not insert_response or "response" not in insert_response:
                
                raise Exception(
                    f"{self.request_id} --- {self.__class__.__name__} -- ERROR: LABEL_PROJECT_INSERT_FAILED")
            
            current_app.logger.info(
                f"{self.request_id} --- {self.__class__.__name__} -- LABEL_PROJECT_CREATED: {insert_response}")

            return {"status": "SUCCESS", "data": {"label_studio_internal_id": label_studio_internal_id, "label_project_id": insert_response["response"]["label_project_id"], "project_title": title}}

        except Exception as e:
            current_app.logger.error(
                f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: {str(e)}")
            current_app.logger.error(
                f"{self.request_id} --- TRACE: {traceback.format_exc()}")
            return {"status": "FAILED", "error": str(e)}
