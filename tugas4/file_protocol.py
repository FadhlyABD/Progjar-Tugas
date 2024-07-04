import json
import logging
import shlex

from file_interface import FileInterface


class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def process_string(self, input_string=''):
        logging.warning(f"Processing string: {input_string}")
        command_parts = shlex.split(input_string)
        try:
            command = command_parts[0].strip().upper()
            logging.warning(f"Processing request: {command}")
            params = [x for x in command_parts[1:]]
            if hasattr(self.file, command.lower()):
                method = getattr(self.file, command.lower())(params)
                return json.dumps(method)
            else:
                return json.dumps(dict(status='ERROR', data='Unknown request'))
        except Exception as e:
            return json.dumps(dict(status='ERROR', data=str(e)))
