from pydantic import BaseModel

class ICreateLabelStudioProject(BaseModel):
    label_studio_project_id: int
    datastore_subset_id: str
    name: str
    description: str
    created_by: str
    result: str