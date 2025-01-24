import json
from flask import Blueprint, current_app, g, jsonify, make_response, request
from flask_cors import CORS

from api_webhook.handler.webhook_handler import WebhookHandler


webhook_api = Blueprint('webhook_api', __name__)
CORS(webhook_api)

@webhook_api.route('/api/webhook-handler/project-update', methods=['POST'])
def project_update():
    data = json.loads(request.data)
    request_id = g.request_id
    handler = WebhookHandler(request_id, data)
    response = handler.do_process()

    return make_response("SUCCESS", 200)
