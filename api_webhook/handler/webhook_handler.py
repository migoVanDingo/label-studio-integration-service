from flask import current_app
from interface.abstract_handler import AbstractHandler


class WebhookHandler(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- WEBHOOK_PAYLOAD: {self.payload}")

            return {"status": "SUCCESS"}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- ERROR: {str(e)}")
            return {"status": "FAILED", "error": str(e)}
        


       