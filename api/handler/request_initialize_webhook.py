import traceback
from flask import current_app

from api.abstract_label_studio import AbstractLabelStudio
from api.entity.payload_initialize_webhook import IInitializeWebhook, PayloadInitializeWebhook
from utility.Constant import Constant


class RequestInitializeWebhook(AbstractLabelStudio):
    def __init__(self, request_id: str, payload: IInitializeWebhook):
        super().__init__()
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- PAYLOAD: {self.payload}")

            response = self.create_webhook(PayloadInitializeWebhook.form_request_payload({
                "actions": Constant.webhook_events,
                "label_studio_internal_id": self.payload["label_studio_internal_id"],
                "url": Constant.base_url + Constant.local_port + Constant.webhook_endpoint
                
            }))

          

            current_app.logger.info(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- RESPONSE: {response}")

            return {"status": "SUCCESS"}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} ERROR: {e}")
            current_app.logger.error(f"{self.request_id} --- TRACE: {traceback.format_exc()}")
            return {"status": "FAILED", "error": str(e)}
        
        