'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Creates database connections.
'''

from ...storage import AppStorage as app_storage

@app_storage(action='read', db_dir='database')
def read_file(self, db_name: str, **kwargs):
    pass

@app_storage(action='update', db_dir='database')
def update_file(self, db_name: str, data: dict, **kwargs):
    pass

@app_storage(action='write', db_dir='database')
def write_file(self, db_name: str, data: dict, **kwargs):
    pass

@app_storage(action='delete', db_dir='database')
def delete_file(self, db_name: str, **kwargs):
    pass