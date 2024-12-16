import time
import traceback
from utility.Constant import Constant
from api.handler.request_create_label_studio_project import RequestCreateLabelStudioProject
from flask import current_app, json
from dao.table_jobs import TableJobs
from dao.table_job_tasks import TableJobTasks

class LabelStudioTasks:

    @staticmethod
    def create_label_studio_project(job_id):

        try:

            current_app.logger.info(f"Job: {__name__} -- job_id: {job_id}")

            # Use job_id to get payload from jobs table
            table_jobs = TableJobs()
            job = table_jobs.get_item_by_id(job_id)

            payload = json.loads(job["payload"])

            # Update jobs table payload with project_id and status as 'in-progress'
            table_job_tasks = TableJobTasks()
            table_job_tasks.update(
                {'job_task_id': get_current_job().id, 'status': 'in-progress'})

            # Create project in Label Studio
            request = RequestCreateLabelStudioProject(payload)
            response = request.do_process()

            # If project creation is successful, update jobs table status as 'completed'
            if response.get('status') == 'success':
                current_app.logger.info(
                    f"Job: {__name__} -- job_id: {job_id} -- response: {response}")
                table_job_tasks.update(
                    {'job_task_id': get_current_job().id, 'status': 'completed'})
                table_jobs.update(
                    {'job_id': job_id, 'payload': json.dumps(response.get('response'))})

            return response

        except Exception as e:
            current_app.logger.error(
                f"Job: {__name__} -- job_id: {job_id} -- Error: {e}")

            # Update jobs table status as 'failed'
            table_jobs.update({'job_id': job_id, 'status': 'failed'})
            table_job_tasks.update(
                {'job_task_id': get_current_job().id, 'status': 'failed'})
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")


    @staticmethod
    def create_label_studio_webhook(job_id):
        current_app.logger.info(f"Job: {__name__} -- job_id: {job_id}")


    @staticmethod
    def create_label_studio_import_storage(job_id):
        current_app.logger.info(f"Job: {__name__} -- job_id: {job_id}")


    @staticmethod
    def sync_label_studio_import_storage(job_id):
        current_app.logger.info(f"Job: {__name__} -- job_id: {job_id}")
