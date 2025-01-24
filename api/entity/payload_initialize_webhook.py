from pydantic import BaseModel

class IInitializeWebhook(BaseModel):
    label_studio_internal_id: int

class IWebhookRequest(BaseModel):
    actions: list
    project: int
    url: str

    headers: dict = {}
    is_active: bool = True
    send_for_all_actions: bool = True
    send_payload: bool = True

class PayloadInitializeWebhook:

    @staticmethod
    def form_payload(data: dict) -> IInitializeWebhook:
        return {
            "label_studio_internal_id": int(data.get("label_studio_internal_id"))
        }


    @staticmethod
    def form_request_payload(data: dict) -> IWebhookRequest:
        return {
            "actions": data.get("actions"),
            "project": data.get("label_studio_internal_id"),
            "url": data.get("url"),

            "headers": {},
            "is_active": True,
            "send_for_all_actions": True,
            "send_payload": True


        }
    
