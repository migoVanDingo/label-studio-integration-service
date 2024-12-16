import traceback
from flask import current_app
from dao.connect import Database
from utility.Utils import Utils


class TableJobTasks:
    def __init__(self):
        connect = Database('BACKEND')
        self.job_tracking_db = connect.get_connection()

    def insert(self, payload):
        try:
            #current_app.logger.debug(f"{self.__class__.__name__}:: payload: {payload}")
            payload["job_task_id"] = Utils.generate_id("TSK")
            query = "INSERT INTO job_tasks (job_id, job_task_id, status, task_name) VALUES (%s, %s, %s, %s)"
            cur = self.job_tracking_db.cursor()
            cur.execute(query, (payload["job_id"], payload["job_task_id"], payload["status"], payload['task_name']))
            self.job_tracking_db.commit()
            cur.close()
            return payload
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return "TableJobTasks -- insert() Error: " + str(e)

            

    def get_list(self, job_id):
        try:
            current_app.logger.debug(f"{self.__class__.__name__} :: job_id: {job_id}")
            query = "SELECT * FROM job_tasks WHERE job_id = %s"
            cur = self.job_tracking_db.cursor()
            cur.execute(query, (job_id,))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return "TableJobTasks -- get_list() Error: " + str(e)
        
    def get_item_by_id(self, job_task_id):
        try:
            current_app.logger.debug(f"{self.__class__.__name__} :: job_task_id: {job_task_id}")
            query = "SELECT * FROM job_tasks WHERE job_task_id = %s"
            cur = self.job_tracking_db.cursor()
            cur.execute(query, (job_task_id,))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return "TableJobTasks -- get_item_by_id() Error: " + str(e)
        
    def find_by(self, fields):
        try:
            current_app.logger.debug(f"{self.__class__.__name__} :: fields: {fields}")
            query = "SELECT * FROM job_tasks WHERE "
            for key in fields.keys():
                query += key + " = %s"
                if list(fields.keys()).index(key) < len(fields.keys()) - 1:
                    query += " AND "

            cur = self.job_tracking_db.cursor()
            cur.execute(query, list(fields.values()))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return "TableJobTasks -- find_item() Error: " + str(e)
        
    def update(self, update_fields, update_values, job_task_id):
        try:
            current_app.logger.debug(f"{self.__class__.__name__} :: update_fields: {update_fields}, update_values: {update_values}, job_id: {job_task_id}")

            query = "UPDATE job_tasks SET "
            for i in range(len(update_fields)):
                query += update_fields[i] + " = %s"
                if i < len(update_fields) - 1:
                    query += ", "
            
            query += " WHERE job_task_id = %s"

            
            cur = self.job_tracking_db.cursor()
            cur.execute(query, update_values + [job_task_id])
            self.job_tracking_db.commit()
            cur.close()
            return True
        
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return False
    
        
