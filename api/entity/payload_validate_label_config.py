from pydantic import BaseModel


class IValidateLabelConfig(BaseModel):
    data_type: str
    labels: list
    fps: int




class PayloadValidateLabelConfig:
    @staticmethod
    def form_payload(data: dict) -> IValidateLabelConfig:
        return {
            "data_type": data.get("type"),
            "labels": data.get("labels"),
            "fps": data.get("fps")
        }