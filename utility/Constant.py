class Constant:
    tasks = {
        "CREATE_PROJECT":"create_label_studio_project",
        "CREATE_WEBHOOK":"create_label_studio_webhook",
        "CREATE_IMPORT_STORAGE":"create_label_studio_import_storage",
        "SYNC_IMPORT_STORAGE":"sync_label_studio_import_storage",
    }

    service_name = "LABEL_STUDIO_INTEGRATION_SERVICE"


Constant.tasks = staticmethod(Constant.tasks)
Constant.service_name = staticmethod(Constant.service_name)