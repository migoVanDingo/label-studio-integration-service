import traceback
from flask import current_app


class InitializeLabelStudioProject:

    def __init__(self, data):
        self.data = data
        self.payload = data["payload"]   

    def do_process(self):
        try:
            


            return None
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} ERROR: {e}")
            current_app.logger.error(f"TRACE: {traceback.format_exc()}")