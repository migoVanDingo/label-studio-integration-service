import json
from flask import current_app
from pydantic import BaseModel


class IValidateProjectConfig(BaseModel):
    label_studio_internal_id: int
    label_config: str

class PayloadValidateProjectConfig:
    @staticmethod
    def form_payload(data: dict) -> IValidateProjectConfig:
        return {
            "label_studio_internal_id": int(data.get("label_studio_internal_id")),
            "label_config": data.get("label_config")
        }
    
    @staticmethod
    def form_request_payload(data: dict) -> IValidateProjectConfig:
        payload = json.dumps({
            "label_config": data.get("label_config")
        })

        current_app.logger.info(f"PayloadValidateProjectConfig: {payload}")
        return payload