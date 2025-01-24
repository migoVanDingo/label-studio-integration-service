from flask import current_app
from api.abstract_label_studio import AbstractLabelStudio
from api.entity.payload_validate_project_config import IValidateProjectConfig, PayloadValidateProjectConfig


class RequestValidateProjectConfig(AbstractLabelStudio):
    def __init__(self, request_id: str, payload: IValidateProjectConfig):
        super().__init__()
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- PAYLOAD: {self.payload}")
            
            response = self.validate_project_label_config(self.payload['label_studio_internal_id'],PayloadValidateProjectConfig.form_request_payload(self.payload))
            current_app.logger.info(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- RESPONSE: {response}")
            # if response.status_code == 201:
            #     return {"status": "SUCCESS"}
            # else:
            #     current_app.logger.error(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: {response['detail']}")
            #     raise Exception(f"{self.request_id} Failed to validate project config")

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: {str(e)}")
            return {"status": "FAILED", "error": str(e)}