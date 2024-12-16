import logging
import os
from flask import Flask, make_response, request
from flask_cors import CORS
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import APIs
from api.label_studio_api import label_studio_api


# Set up logging
logging.basicConfig(filename='record.log',
                    level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s')

app = Flask(__name__)
CORS(app)


# Send OPTIONS for POST requests
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response('success', 200)
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = '*'
        return response
    

# Register REST APIs
app.register_blueprint(label_studio_api)


if __name__ == '__main__':
    app.run(debug=True, port = os.environ.get('PORT'))