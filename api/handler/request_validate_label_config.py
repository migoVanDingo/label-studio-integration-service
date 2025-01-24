import json
import traceback
from flask import current_app
from api.abstract_label_studio import AbstractLabelStudio
from api.entity.payload_validate_label_config import IValidateLabelConfig
from classes.label_studio import LabelStudio
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError


"""
    Class RequestValidateLabelConfig:
    - This class is responsible for validating the label config for a label studio project
    - In the Label Studio UI, the label config is where your labels, FPS and label project type (video tracking/classification etc) are defined
    - Used in job-flow, or as standalone request handler.

    Super: AbstractLabelStudio
    - The abstract class which contains the abstracted Label Studio methods
    - These methods will form the payloads/headers/urls etc for interacting with the LabelStudio API

    Payload:
    class IValidateLabelConfig(BaseModel):
        data_type: str
        labels: list
        fps: int

    Return:
    class ReturnValidateLabelConfig:
        label_config: str

    
"""
""" 
class ReturnValidateLabelConfig:
    label_config: str """


class RequestValidateLabelConfig(AbstractHandler, AbstractLabelStudio):
    def __init__(self, request_id: str, payload: IValidateLabelConfig):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- VALIDATE_LABEL_CONFIG:::PAYLOAD: {self.payload}")

            if "data_type" not in self.payload:
                current_app.logger.error(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: DATA_TYPE_NOT_FOUND")
                raise Exception(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: DATA_TYPE_NOT_FOUND")
            
            match self.payload["data_type"]:
                case "video":
                    label_config = LabelStudio.create_label_config_video(self.payload["labels"], self.payload["fps"])
                case "image":
                    raise Exception(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: IMAGE NOT_IMPLEMENTED")
                case "audio":
                    raise Exception(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: AUDIO NOT_IMPLEMENTED")
                case _:
                    raise Exception(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: DATA_TYPE_NOT_FOUND")
                
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- LABEL_CONFIG: {label_config}")

            if label_config["status"] != "SUCCESS":
                current_app.logger.error(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: {label_config['error']}")
                raise Exception(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- Label Config Generation Failed ERROR: {label_config['error']}")
            
            validate = self.validate_label_config(json.dumps({"label_config":label_config["data"]}))

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- VALIDATE_LABEL_CONFIG_RESPONSE: {validate}")

            # if response statuse is 204
            if validate.status_code == 204:
                return {"status":"SUCCESS", "data":{"label_config": label_config["data"] }}
            else:
                raise Exception(f"{self.request_id} --- CLASS: {self.__class__.__name__} --- LABEL_CONFIG_VALIDATION_FAILED")

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {traceback.format_exc()} --- CLASS: {self.__class__.__name__} -- ERROR: {str(e)}")
            return {"status": "FAILED", "error": str(e)}