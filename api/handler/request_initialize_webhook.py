import traceback
from flask import current_app
import requests

from api.abstract_label_studio import AbstractLabelStudio


class RequestInitializeWebhook(AbstractLabelStudio):
    def __init__(self, payload):
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"CLASS: {self.__class__.__name__} -- PAYLOAD: {self.payload}")
            payload_create_webhook = {
                "actions": [
                    "PROJECT_UPDATED"
                ],
                "headers": {},
                "is_active": True,
                "project": int(self.payload['label_studio_project_id']),
                "send_for_all_actions": True,
                "send_payload": True,
                "url": "http://127.0.0.1:5003/api/webhook-handler/project-created"
            }

            response = self.create_webhook(payload_create_webhook)

            current_app.logger.info(f"CLASS: {self.__class__.__name__} -- RESPONSE: {response.json()}")


            return {"status": "success", "data": response.json()}

        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} ERROR: {e}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return {"status": "failed", "error": str(e)}
        
        