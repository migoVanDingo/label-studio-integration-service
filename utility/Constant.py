class Constant:
    service_name = "LABEL_STUDIO_INTEGRATION_SERVICE"
    

    labeler_output_dir = "/Users/bubz/Developer/master-project/tests/test-labeler-output"
    webhook_endpoint = "/api/webhook-handler/project-update"
    webhook_events = ["PROJECT_UPDATED"]
    local_port = "5016"
    label_studio_user_token = "4bf3e0cdb26c83f497c291750f634ce23198342f"

    base_url = "http://localhost:"
    local_port = "8080"
    dao_port = "5010"

    dao = {
        "create": "/api/create",
        "read": "/api/read",
        "list": "/api/read_list",
        "update": "/api/update",
        "delete": "/api/delete",
        "read_all": "/api/read_all",
        "query": "/api/query"
    }

    table = {
        "DATASTORE": "datastore",
        "DATASTORE_ROLES": "datastore_roles",
        "DATASET": "dataset",
        "DATASET_ROLES": "dataset_roles",
        "FILES": "files",
        "DATASTORE_CONFIG": "datastore_config",
        "DATASET_FILES": "dataset_files",
        "LABEL_PROJECT": "label_project",
    }

    delimeter = {
        "DATASTORE": "__",
        "DATASET": "__"
    }

   
    tasks = {
            "CREATE_PROJECT":"create_label_studio_project",
            "CREATE_WEBHOOK":"create_label_studio_webhook",
            "CREATE_IMPORT_STORAGE":"create_label_studio_import_storage",
            "SYNC_IMPORT_STORAGE":"sync_label_studio_import_storage",
        }

    
Constant.tasks = staticmethod(Constant.tasks)
Constant.service_name = staticmethod(Constant.service_name)