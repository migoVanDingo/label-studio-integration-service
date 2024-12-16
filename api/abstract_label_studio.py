from abc import ABC, abstractmethod
import os, json
import requests
from dotenv import load_dotenv

from dao.table_label_studio_project import TableLabelStudioProject
load_dotenv()


class AbstractLabelStudio(ABC):
    def __init__(self):
        super().__init__()
        self.table_label_studio_project = TableLabelStudioProject()
        self.token=os.environ['LABEL_STUDIO_USER_TOKEN']

    def get_token(self):
        return os.environ['LABEL_STUDIO_USER_TOKEN']

    def get_headers(self):
        headers = {
            "Authorization":"Token {}".format(self.get_token()),
            "Content-Type": "application/json"
        }

        return headers
    
    def get_webhook_headers(self):
        webhook_headers = {
            "Authorization":"Token {}".format(self.get_token())
        }
        return webhook_headers


    def endpoint_url_create_label_studio_project(self):
        return "http://localhost:8080/api/projects"
    
    def endpoint_url_create_webhook(self):
        return "http://localhost:8080/api/webhooks"
    
    def endpoint_url_get_project_list(self):
        return "http://localhost:8080/api/projects"
    
    def endpoint_url_get_label_studio_project(self, label_studio_project_id):
        return "http://localhost:8080/api/projects/{}".format(label_studio_project_id)
    
    def endpoint_url_update_label_studio_project(self, label_studio_project_id):
        return "http://localhost:8080/api/projects/{}".format(label_studio_project_id)
    
    def endpoint_url_delete_label_studio_project(self, label_studio_project_id):
        return "http://localhost:8080/api/projects/{}".format(label_studio_project_id)
    
    def endpoint_validate_label_config(self):
        return "http://localhost:8080/api/projects/validate"
    
    def endpoint_url_create_import_storage(self):
        return "http://localhost:8080/api/storages/localfiles"
    
    def endpoint_url_sync_import_storage(self, local_storage_id):
        return "http://localhost:8080/api/storages/localfiles/{}/sync".format(local_storage_id)
    
    def endpoint_url_get_all_frames(self, project_id):
        return "http://localhost:8080/api/projects/"+ str(project_id) +"/export?exportType=JSON&interpolate_key_frames=true"
    




    #Requests
    def post(self, url, payload, headers):
        return requests.post(url, data=payload, headers=headers)
    
    def get(self, url, headers):
        return requests.get(url, headers=headers)
    
    def patch(self, url, payload, headers):
        return requests.patch(url, data=payload, headers=headers)
    
    def delete(self, url, headers):
        return requests.delete(url, headers=headers)



    # Interact with Label Studio
    def create_label_studio_project(self, payload):
        return self.post(self.endpoint_url_create_label_studio_project(), payload, self.get_headers()).json()

    def get_label_studio_project_list(self):
        return self.get(self.endpoint_url_get_project_list(), self.get_headers())

    def get_label_studio_project(self, label_studio_project_id):
        return self.get(self.endpoint_url_get_label_studio_project(label_studio_project_id), self.get_headers())

    def update_label_studio_project(self, label_studio_project_id, payload):
        return self.patch(self.endpoint_url_update_label_studio_project(label_studio_project_id), payload, self.get_headers())

    def delete_label_studio_project(self, label_studio_project_id):
        return self.delete(self.endpoint_url_delete_label_studio_project(label_studio_project_id), self.get_headers())

    def validate_label_config(self, config):
        return self.post(self.endpoint_validate_label_config(), config, self.get_headers())
    
    def create_webhook(self, payload):
        return self.post(self.endpoint_url_create_webhook(), payload, headers=self.get_webhook_headers())
    
    def create_import_storage(self, payload):
        return self.post(self.endpoint_url_create_import_storage(), payload, self.get_headers())
    
    def sync_import_storage(self, local_storage_id, payload):
        return self.post(self.endpoint_url_sync_import_storage(local_storage_id), payload, self.get_headers())


    @abstractmethod
    def do_process(self):
        pass