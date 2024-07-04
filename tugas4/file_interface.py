import os
import json
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self, params=[]):
        try:
            file_list = glob('*.*')
            return dict(status='OK', data=file_list)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if not filename:
                return None
            with open(f"{filename}", 'rb') as file:
                file_content = base64.b64encode(file.read()).decode()
            return dict(status='OK', filename=filename, file_content=file_content)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def upload(self, params=[]):
        try:
            filename = params[0]
            file_data = base64.b64decode(params[1])
            with open(f"{filename}", 'wb') as file:
                file.write(file_data)
            return dict(status='OK', data='File uploaded successfully')
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=[]):
        try:
            filename = params[0]
            if os.path.exists(filename):
                os.remove(filename)
                return dict(status='OK', data='File deleted successfully')
            else:
                return dict(status='ERROR', data='File not found')
        except Exception as e:
            return dict(status='ERROR', data=str(e))
