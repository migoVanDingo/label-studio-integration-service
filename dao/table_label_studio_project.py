""" import traceback
from flask import current_app
from dao.connect import Database
from utility.Utils import Utils
from api.entity.interface_create_label_studio_project import ICreateLabelStudioProject

class TableLabelStudioProject:
    def __init__(self):
        connect = Database('BACKEND')
        self.label_studio_service_db = connect.get_connection()

    def insert(self, payload: ICreateLabelStudioProject):
        try:
            payload["ls_id"] = Utils.generate_id("LSP")
            current_app.logger.debug(f"CLASS: {self.__class__.__name__} -- DAO -- PAYLOAD: {payload}")

            query = "INSERT INTO label_studio_project (ls_id, label_studio_project_id, datastore_subset_id, name, description, created_by, result, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, 1)"
            cur = self.label_studio_service_db.cursor()
            cur.execute(query, (payload["ls_id"], payload["label_studio_project_id"], payload["datastore_subset_id"], payload["name"], payload["description"], payload['created_by'], payload['result']))
            self.label_studio_service_db.commit()
            cur.close()
        
            return payload
        

        except Exception as e:
            current_app.logger.error(f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}"
        
    def get_item_by_id(self, ls_id):
        try:
            current_app.logger.debug(f"CLASS: {self.__class__.__name__} -- DAO -- ls_id: {ls_id}")
            query = "SELECT * FROM label_studio_project WHERE ls_id = %s"
            cur = self.label_studio_service_db.cursor()
            cur.execute(query, (ls_id,))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            current_app.logger.error(f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}"
        
    def find_by(self, fields):
        try:
            current_app.logger.debug(f"CLASS: {self.__class__.__name__} -- DAO -- fields: {fields}")
            query = "SELECT * FROM label_studio_project WHERE "
            for key in fields.keys():
                query += key + " = %s"
                if list(fields.keys()).index(key) < len(fields.keys()) - 1:
                    query += " AND "

            cur = self.label_studio_service_db.cursor()
            cur.execute(query, list(fields.values()))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as e:
            current_app.logger.error(f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}"
        
    def update(self, update_fields, update_values, ls_id):
        try:
            query = "UPDATE label_studio_project SET "
            for i in range(len(update_fields)):
                query += update_fields[i] + " = %s"
                if i < len(update_fields) - 1:
                    query += ", "

            query += " WHERE ls_id = %s"
   
            cur = self.label_studio_service_db.cursor()
            cur.execute(query, update_values + [ls_id])
            self.label_studio_service_db.commit()
            cur.close()
            return { "status":"success" , "ls_id":ls_id}

        except Exception as e:
            current_app.logger.error(f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}"
        
    def delete(self, ls_id):
        try:
            current_app.logger.debug(f"CLASS: {self.__class__.__name__} -- DAO -- ls_id: {ls_id}")
            query = "UPDATE label_studio_project SET is_active = 0 WHERE ls_id = %s"
            cur = self.label_studio_service_db.cursor()
            cur.execute(query, (ls_id,))
            self.label_studio_service_db.commit()
            cur.close()
            return ls_id
        except Exception as e:
            current_app.logger.error(f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")
            return f"CLASS: {self.__class__.__name__} -- DAO -- ERROR: {str(e)}" """