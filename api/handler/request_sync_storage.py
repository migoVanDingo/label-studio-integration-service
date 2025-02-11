from flask import current_app

from api.abstract_label_studio import AbstractLabelStudio
from api.entity.payload_sync_import_storage import ISyncImportStorage


class RequestSyncImportStorage(AbstractLabelStudio):

    def __init__(self, request_id: str, payload: ISyncImportStorage):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- SYNC_IMPORT_STORAGE_PAYLOAD: {self.payload}")

            response = self.sync_import_storage(self.payload['import_storage_id'])

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- SYNC_IMPORT_STORAGE_RESPONSE: {response}")

            
            
            return {"status": "SUCCESS"}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- CLASS: {self.__class__.__name__} -- ERROR: {str(e)}")
            return {"status": "FAILED", "error": str(e)}