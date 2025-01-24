import json
from typing import Optional
from flask import current_app
from pydantic import BaseModel


class IInitializeImportStorage(BaseModel):
    label_studio_internal_id: int
    label_project_id: str
    project_title: str
    set_path: str
    datastore_id: str
    set_id: str
    data_type: str

class IImportStorageRequest(BaseModel):
    title: str
    description: Optional[str] = None
    project: int
    path: str
    use_blob_urls: bool = True


class PayloadInitializeImportStorage:
    @staticmethod
    def form_payload(data: dict) -> IInitializeImportStorage:
        return {
            "label_studio_internal_id": int(data.get("label_studio_internal_id")),
            "project_title": data.get("project_title") + "_Import_Storage",
            "set_path": data.get("set_path"),
            "datastore_id": data.get("datastore_id"),
            "set_id": data.get("set_id"),
            "data_type": data.get("data_type"),
            "label_project_id": data.get("label_project_id")
        }
    
    @staticmethod
    def form_request_payload(data: dict) -> IImportStorageRequest:
        payload =  {
            "title": data.get("project_title"),
            "description": "",
            "project": data.get("label_studio_internal_id"),
            "path": data.get("set_path"),
            "use_blob_urls": True
        }

        current_app.logger.info(f"REQUEST PAYLOAD: {payload}")
        return json.dumps(payload)