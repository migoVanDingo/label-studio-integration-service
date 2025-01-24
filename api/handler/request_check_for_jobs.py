""" import traceback
from flask import current_app, json

from api.handler.request_create_label_studio_project import RequestCreateLabelStudioProject
from api.handler.request_initialize_import_storage import RequestInitializeImportStorage
from api.handler.request_initialize_webhook import RequestInitializeWebhook
from api.handler.request_sync_storage import RequestSyncStorage
from dao.table_job_tasks import TableJobTasks
from dao.table_jobs import TableJobs


class RequestCheckForJobs:

    def __init__(self):
        self.table_jobs = TableJobs()
        self.table_job_tasks = TableJobTasks()

    def do_process(self):
        try:
            current_app.logger.info(f"CLASS: {self.__class__.__name__} -- Checking for jobs..........")
            jobs = self.table_jobs.find_by(['status','service'], ['pending', 'LABEL_STUDIO_INTEGRATION_SERVICE'])

            if jobs:
                for job in jobs:
                    self.table_jobs.update(['status'], ['in-progress'], job['job_id'])

                    # Run job
                    return self.run_job_tasks(job)
            else:
                return {"status": "success", "message": "NO_JOBS_FOUND"}

            


        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} ERROR: {e}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return {"status": "failed", "error": str(e)}
        
    
    def run_job_tasks(self, job):
        
        checklist = []
        payload = json.loads(job['data'])

        for index, task in enumerate(json.loads(job['tasks'])):
            if job['service'] == 'LABEL_STUDIO_INTEGRATION_SERVICE':

                insert_task = self.table_job_tasks.insert({'job_id': job['job_id'], 'task_name': task, 'status': 'in-progress'})
                match task:
                    
                    case 'create_label_studio_project':
                        request = RequestCreateLabelStudioProject(payload)
                        response = request.do_process()

                    case 'create_label_studio_webhook':
                        request = RequestInitializeWebhook(payload)
                        response = request.do_process()


                    case 'create_label_studio_import_storage':
                        request = RequestInitializeImportStorage(payload)
                        response = request.do_process()


                    case 'sync_label_studio_import_storage':
                        request = RequestSyncStorage(payload)
                        response = request.do_process()

                    case _:
                        current_app.logger.error(f"Task: {task} not found")
                        break
                
                if response["status"] == "success":
                    checklist.append({"task": task, "status": "completed"})

                    self.table_job_tasks.update(['status', 'result'], ['completed', response], insert_task['job_task_id'])

                    payload = response["data"]

                else:
                    self.table_jobs.update(['status', 'result', 'error'], ['failed', task, response['error']], job['job_id'])

                    self.table_job_tasks.update(['status', 'error'], ['failed', response['error']], insert_task['job_task_id'])

                    return {"status": "failed", "error": response['error']}


        return checklist """