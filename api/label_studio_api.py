from flask import Blueprint, json, request
from flask_cors import CORS

from api.handler.Initialize_label_studio_project import InitializeLabelStudioProject
from api.handler.request_check_for_jobs import RequestCheckForJobs

from api.handler.request_get_label_studio_info import RequestGetLabelStudioInfo


label_studio_api = Blueprint('label_studio_api', __name__)
CORS(label_studio_api)


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
