from pydantic import BaseModel


class ISyncImportStorage(BaseModel):
    import_storage_id: int
    label_studio_internal_id: int

class ISyncImportStorageRequest(BaseModel):
    label_studio_internal_id: int
    use_blob_urls: bool = True

class PayloadSyncImportStorage:
    @staticmethod
    def form_payload(data: dict) -> ISyncImportStorage:
        return {
            "import_storage_id": int(data.get("import_storage_id")),
            "label_studio_internal_id": int(data.get("label_studio_internal_id"))
        }
    
    @staticmethod
    def form_request_payload(data: dict) -> ISyncImportStorageRequest:
        return {
            "label_studio_internal_id": int(data.get("label_studio_internal_id")),
            "use_blob_urls": data.get("use_blob_urls")
        }