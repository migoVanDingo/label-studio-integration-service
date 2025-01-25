class JobPayload:
    @staticmethod
    def form_job_payload(payload: dict, description: dict):
        return {
                "user_id": description.get("user_id"),
                "project_name": description.get("project_name"),
                "dataset_id": description.get("dataset_id"),
                "datastore_id": description.get("datastore_id"),
                "set_id": description.get("set_id"),
                "task_id": payload.get("task")["id"],
                "project_id": payload.get("project")["id"],
                "dataset_directory_path": payload.get("dataset_directory_path"),
                "set_name": payload.get("set_name"),
                "label_project_id": payload.get("label_project_id"),
                "file_name": payload.get("file_name"),
                "job_name": "HANDLE_LABEL_PROJECT_UPDATE"
            } 