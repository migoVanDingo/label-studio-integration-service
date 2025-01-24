from flask import current_app
from api.abstract_label_studio import AbstractLabelStudio


class RequestDeleteProjects(AbstractLabelStudio):
    def __init__(self):
        pass

    def do_process(self):
        try:
            value = 678
            while value > 670:
                current_app.logger.info(f"DELETING PROJECTS: {value}")
                self.delete_project(value)
   
                value -= 1
                
            return {"status": "SUCCESS"}
        except Exception as e:
            current_app.logger.error(f"ERROR: {e}")
            return {"status": "FAILED", "error": str(e)}