from flask import Blueprint, g, json, request
from flask_cors import CORS

from api.handler.Initialize_label_studio_project import InitializeLabelStudioProject
from api.handler.request_check_for_jobs import RequestCheckForJobs

from api.handler.request_create_label_studio_project import RequestCreateLabelStudioProject
from api.handler.request_get_label_studio_info import RequestGetLabelStudioInfo
from api.handler.request_initialize_import_storage import RequestInitializeImportStorage
from api.handler.request_initialize_webhook import RequestInitializeWebhook
from api.handler.request_sync_storage import RequestSyncImportStorage
from api.handler.request_validate_label_config import RequestValidateLabelConfig


label_studio_api = Blueprint('label_studio_api', __name__)
CORS(label_studio_api)

@label_studio_api.route('/api/label-project/new', methods=['POST'])
def create_label_project():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data["request_id"]
    else:
        request_id = g.request_id
    
    request = RequestCreateLabelStudioProject(request_id, data)
    response = request.do_process()
    return response


# Init import storage
@label_studio_api.route('/api/label-project/import-storage', methods=['POST'])
def create_import_storage():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data["request_id"]
    else:
        request_id = g.request_id
    
    request = RequestInitializeImportStorage(request_id, data)
    response = request.do_process()
    return response

# Sync Import Storage
@label_studio_api.route('/api/label-project/import-storage/sync', methods=['POST'])
def sync_import_storage():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data["request_id"]
    else:
        request_id = g.request_id
    
    request = RequestSyncImportStorage(request_id, data)
    response = request.do_process

# Init webhook
@label_studio_api.route('/api/label-project/webhook', methods=['POST'])
def create_webhook():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data["request_id"]
    else:
        request_id = g.request_id
    
    request = RequestInitializeWebhook(request_id, data)
    response = request.do_process()
    return response


# Validate Project Label Config
@label_studio_api.route('/api/label-project/validate-config', methods=['POST'])
def validate_label_config():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data["request_id"]
    else:
        request_id = g.request_id
    
    request = RequestValidateLabelConfig(request_id, data)
    response = request.do_process()
    return response








@label_studio_api.route('/api/label_studio', methods=['POST'])
def initialize_label_studio_project():
    data = json.loads(request.data)

    request = InitializeLabelStudioProject(data)
    response = request.do_process()
    return response


@label_studio_api.route('/api/label_studio', methods=['GET'])
def get_label_studio_project_info():
    if request.args.get('subset_id') is not None:
        subset_id = request.args.get('subset_id')
        
    if request.args.get('project_id') is not None:
        project_id = request.args.get('project_id')

    api_request = RequestGetLabelStudioInfo(subset_id, project_id)
    response = api_request.do_process()
    return response

@label_studio_api.route('/api/label_studio/job', methods=['GET'])
def receive_job():

    request = RequestCheckForJobs()
    response = request.do_process()
    return response    
