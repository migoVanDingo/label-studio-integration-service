from flask_mysqldb import MySQL
from flask import current_app

class Database:
    def __init__(self, database):
        # Initialize database settings
        from app import app  # Get the current Flask app context
        self.app = app
        self.mysql = MySQL()
        self.mysql_host = None
        self.mysql_user = None
        self.mysql_password = None
        self.mysql_db = None
        self.mysql_cursorclass = None
        self.prepare_connection(database)

    def prepare_connection(self, database):
        # Dynamically configure based on the database name
        match database:
            case 'BACKEND':
                self.prepare_aolme_db_v2_connection()
            case 'LABEL_STUDIO_SERVICE':
                self.prepare_label_studio_connection()
            case 'JOB_TRACKING':
                self.prepare_job_tracking_connection()
            case _:
                self.prepare_aolme_db_v2_connection()

        # Apply the database configuration to the Flask app
        self.app.config['MYSQL_HOST'] = self.mysql_host
        self.app.config['MYSQL_USER'] = self.mysql_user
        self.app.config['MYSQL_PASSWORD'] = self.mysql_password
        self.app.config['MYSQL_DB'] = self.mysql_db
        self.app.config['MYSQL_CURSORCLASS'] = self.mysql_cursorclass

        # Initialize the MySQL connection with the Flask app config
        self.mysql.init_app(self.app)

    def prepare_aolme_db_v2_connection(self):
        self.mysql_host = 'localhost'
        self.mysql_user = 'aolme_db_v2'
        self.mysql_password = 'password'
        self.mysql_db = 'aolme_db_v2'
        self.mysql_cursorclass = 'DictCursor'

    def prepare_label_studio_connection(self):
        self.mysql_host = 'localhost'
        self.mysql_user = 'label_studio_integration_service'
        self.mysql_password = 'password'
        self.mysql_db = 'label_studio_integration_service'
        self.mysql_cursorclass = 'DictCursor'

    def prepare_job_tracking_connection(self):
        self.mysql_host = 'localhost'
        self.mysql_user = 'job_tracking_service'
        self.mysql_password = 'password'
        self.mysql_db = 'job_tracking_service'
        self.mysql_cursorclass = 'DictCursor'

    def get_connection(self):
        # Explicitly connect to the database before returning the connection
        with self.app.app_context():  # Ensure the app context is active
            connection = self.mysql.connect  # Get the actual connection object
            return connection
