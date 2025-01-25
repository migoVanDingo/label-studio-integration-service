from flask import Blueprint, current_app, g, json, request
from flask_cors import CORS

from api.entity.payload_create_label_studio_project import PayloadCreateLabelStudioProject
from api.entity.payload_initialize_import_storage import PayloadInitializeImportStorage
from api.entity.payload_initialize_webhook import PayloadInitializeWebhook
from api.entity.payload_sync_import_storage import PayloadSyncImportStorage
from api.entity.payload_validate_label_config import PayloadValidateLabelConfig
from api.entity.payload_validate_project_config import PayloadValidateProjectConfig
from api.handler.Initialize_label_studio_project import InitializeLabelStudioProject


from api.handler.request_create_label_studio_project import RequestCreateLabelStudioProject
from api.handler.request_delete_projects import RequestDeleteProjects
from api.handler.request_get_label_projects_list import RequestGetLabelProjectsList
from api.handler.request_get_label_studio_info import RequestGetLabelStudioInfo
from api.handler.request_initialize_import_storage import RequestInitializeImportStorage
from api.handler.request_initialize_webhook import RequestInitializeWebhook
from api.handler.request_launch_labeler import RequestLaunchLabeler
from api.handler.request_pull_annotation_all_frames import RequestPullAnnotationAllFrames
from api.handler.request_sync_storage import RequestSyncImportStorage
from api.handler.request_validate_label_config import RequestValidateLabelConfig
from api.handler.request_validate_project_config import RequestValidateProjectConfig
from api.handler.request_verify_temp_output_path import RequestVerifyTempOutputPath


label_studio_api = Blueprint('label_studio_api', __name__)
CORS(label_studio_api)

#test delete
@label_studio_api.route('/api/delete/yo', methods=['GET'])
def delete_yo():
    response = RequestDeleteProjects().do_process()
    return response


# Validate Config
@label_studio_api.route('/api/label-project/validate-config', methods=['POST'])
def validate_label_config():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id
    
    api_request = RequestValidateLabelConfig(request_id, PayloadValidateLabelConfig.form_payload(data))
    response = api_request.do_process()

    if response["status"] == "SUCCESS":
        res_data = response["data"]
        res_data.update(data)
        return { "status": "SUCCESS", "data": res_data}
    
    return response
    

@label_studio_api.route('/api/label-project/new', methods=['POST'])
def create_label_project():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id
    
    api_request = RequestCreateLabelStudioProject(request_id, PayloadCreateLabelStudioProject.form_payload(data))
    response = api_request.do_process()
    
    if response["status"] == "SUCCESS":
        res_data = response["data"]
        res_data.update(data)
        return { "status": "SUCCESS", "data": res_data}
  
    return response


# Validate Project Label Config
@label_studio_api.route('/api/label-project/validate-config/project', methods=['POST'])
def validate_project_config():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id
    
    api_request = RequestValidateProjectConfig(request_id, PayloadValidateProjectConfig.form_payload(data))
    response = api_request.do_process()

    if response["status"] == "SUCCESS":
        return { "status": "SUCCESS", "data": data}
    
    return response
    

# Init webhook
@label_studio_api.route('/api/label-project/webhook', methods=['POST'])
def create_webhook():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id
    
    api_request = RequestInitializeWebhook(request_id, PayloadInitializeWebhook.form_payload(data))
    response = api_request.do_process()

    if response["status"] == "SUCCESS":
        return { "status": response["status"], "data": data}

    return response


# Init import storage
@label_studio_api.route('/api/label-project/import-storage', methods=['POST'])
def create_import_storage():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id
    
    api_request = RequestInitializeImportStorage(request_id, PayloadInitializeImportStorage.form_payload(data))
    response = api_request.do_process()

    if response["status"] == "SUCCESS":
        res_data = response["data"]
        res_data.update(data)
        return { "status": response["status"], "data": res_data}
    
    return response


# Sync Import Storage
@label_studio_api.route('/api/label-project/import-storage/sync', methods=['POST'])
def sync_import_storage():

    
    data = json.loads(request.data)
    current_app.logger.info(f"SYNC_REQUEST_DATA: {data}")
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id

    current_app.logger.info(f"SYNC_REQUEST_ID: {request_id}")
    
    api_request = RequestSyncImportStorage(request_id, PayloadSyncImportStorage.form_payload(data))
    response = api_request.do_process()

    if "status" in response and response["status"] == "SUCCESS":
        return { "status": response["status"], "data": data}
    
    return response



# Pull all frames from Label Studio
@label_studio_api.route('/api/label-project/pull/annotation/all-frames', methods=['POST'])
def pull_all_frames():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id
    
    api_request = RequestPullAnnotationAllFrames(request_id, data)
    response = api_request.do_process()

    if response["status"] == "SUCCESS":
        res_data = response["data"]
        res_data.update(data)
        return { "status": response["status"], "data": res_data}

    return response


# Verify Temporary Output Directory
@label_studio_api.route('/api/label-project/temp-output/verify', methods=['POST'])
def verify_temp_output():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id
    
    api_request = RequestVerifyTempOutputPath(request_id, data)
    response = api_request.do_process()

    if response["status"] == "SUCCESS":
        res_data = response["data"]
        res_data.update(data)
        return { "status": response["status"], "data": res_data}

    return response







@label_studio_api.route('/api/label-project/list', methods=['GET'])
def get_label_projects_list():
    args = request.args.to_dict()
    if "request_id" in args:
        request_id = args['request_id']
    elif "job_id" in args:
        request_id = args['job_id']
    else:
        request_id = g.request_id

    api_request = RequestGetLabelProjectsList(request_id, args)
    response = api_request.do_process()

    return response


@label_studio_api.route('/api/label-project/launch', methods=['GET'])
def launch_label_studio():
    args = request.args.to_dict()
    project_id = args["project_id"]

    request_id = g.request_id

    api_request = RequestLaunchLabeler(request_id, project_id)
    response = api_request.do_process()

    return response

    
