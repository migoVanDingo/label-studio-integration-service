from typing import Optional
from pydantic import BaseModel


class ICreateLabelProject(BaseModel):
    set_name: str
    set_id: str
    project_name: str
    label_config: str
    datastore_id: str
    description: str
    config_order: list
    instructions: Optional[str]
    dataset_directory_path: str
    user_id: str
    dataset_id: str

class ILabelStudioProject(BaseModel):
    title: str
    description: str
    label_config: str
    expert_instruction: str

class IInsertLabelProject(BaseModel):
    label_studio_internal_id: int
    label_studio_project_name: str
    set_id: str
    datastore_id: str
    set_name: str
    project_name: str
    metadata: str
    label_config: str
    dataset_directory_path: str
    user_id: str
    dataset_id: str
    annotation_output_path: str
    updated_by: str



class PayloadCreateLabelStudioProject:
    @staticmethod
    def form_payload(data: dict) -> ICreateLabelProject:
        base_payload = {
            "set_name": data.get("set_name"),
            "project_name": data.get("project_name"),
            "label_config": data.get("label_config"),
            "datastore_id": data.get("datastore_id"),
            "description": data.get("description"),
            "config_order": data.get("config_order"),
            "instructions": data.get("instructions"),
            "dataset_directory_path": data.get("dataset_directory_path"),
            "set_id": data.get("set_id"),
            "dataset_id": data.get("dataset_id"),
            "user_id": data.get("user_id")
            

        }

        if "config_order" in data:
            for item in data["config_order"]:
                base_payload[item["field_name"]] = data[item["field_name"]]


        return base_payload
    
    @staticmethod
    def form_label_studio_project_payload(title, description, label_config, instructions = "") -> ILabelStudioProject:
        return {
            "title": title,
            "description": description,
            "label_config": label_config,
            "show_instruction": True if instructions != "" else False,
            "expert_instruction": instructions
        }
    
    @staticmethod
    def form_insert_payload(data: dict) -> IInsertLabelProject:
        return {
            "label_studio_internal_id": int(data["label_studio_internal_id"]),
            "label_studio_project_name": data["label_studio_project_name"],
            "set_id": data["set_id"],
            "datastore_id": data["datastore_id"],
            "set_name": data["set_name"],
            "project_name": data["project_name"],
            "metadata": data["metadata"],
            "label_config": data["label_config"],
            "created_by": data["user_id"],
            "dataset_id": data["dataset_id"],
            "dataset_directory_path": data["dataset_directory_path"],
            "updated_by": data["user_id"]

        }
    
    