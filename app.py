import logging
import os
import uuid
from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api_webhook.webhook_api import webhook_api
from utility.error import ThrowError


# Import APIs
from api.label_studio_api import label_studio_api


# Set up logging
logging.basicConfig(filename='record.log',
                    level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s')

def create_app():
    app = Flask(__name__)
    CORS(app)

    #Register blueprints
    app.register_blueprint(label_studio_api)  
    app.register_blueprint(webhook_api)

    return app

app = create_app()


# Send OPTIONS for POST requests
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response('success', 200)
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = '*'
        return response
    else:
        request_id = str(uuid.uuid4())
        g.request_id = request_id


@app.errorhandler(ThrowError)
def handle_throw_error(error):
    response = jsonify({
        "message": str(error),
        "error_code": error.status_code
    })
    response.status_code = error.status_code
    return response



if __name__ == '__main__':
    app.run(debug=True, port = os.environ.get('PORT'))