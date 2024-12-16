import traceback
from flask import current_app, jsonify

from dao.connect import Database

class TableJobs:
    def __init__(self):
        connect = Database('BACKEND')
        self.job_tracking_db = connect.get_connection()
        
    def get_list(self):
        try:
            query = "SELECT * FROM jobs"
            cur = self.job_tracking_db.cursor()
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return "TableJobs -- get_list() Error: " + str(e)
        
    def get_item_by_id(self, job_id):
        try:
            current_app.logger.debug(f"{self.__class__.__name__} :: job_id: {job_id}")
            query = "SELECT * FROM jobs WHERE job_id = %s"
            cur = self.job_tracking_db.cursor()
            cur.execute(query, (job_id,))
            data = cur.fetchone()
            cur.close()
            return data
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return "TableJobs -- get_item_by_id() Error: " + str(e)
        

    def find_by(self, fields, values):
        try:
            
            query = "SELECT * FROM jobs WHERE "
            for i in range(len(fields)):
                query += fields[i] + " = %s"
                if i < len(fields) - 1:
                    query += " AND "
            current_app.logger.debug(f"{self.__class__.__name__} :: query: {query}")
            cur = self.job_tracking_db.cursor()
            cur.execute(query, values)
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return "TableJobs -- find_by() Error: " + str(e)
        
    def update(self, update_fields, update_values, job_id):
        try:
            current_app.logger.debug(f"{self.__class__.__name__} :: update_fields: {update_fields}, update_values: {update_values}, job_id: {job_id}")

            query = "UPDATE jobs SET "
            for i in range(len(update_fields)):
                query += update_fields[i] + " = %s"
                if i < len(update_fields) - 1:
                    query += ", "
            
            query += " WHERE job_id = %s"

            
            cur = self.job_tracking_db.cursor()
            cur.execute(query, update_values + [job_id])
            self.job_tracking_db.commit()
            cur.close()
            return True
        
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :: ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return False
        

