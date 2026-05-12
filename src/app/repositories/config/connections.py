'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Creates database connections.
'''

from typing import Optional

from ...storage import AppStorage as app_storage

def read_file(**kwargs):
    @app_storage(action='read', **kwargs)
    def _read(**kwargs):
        pass
    return _read(**kwargs)

def update_file(**kwargs):
    @app_storage(action='update', **kwargs)
    def _update(**kwargs):
        pass
    return _update(**kwargs)

def write_file(**kwargs):
    @app_storage(action='write', **kwargs)
    def _write(**kwargs):
        pass
    return _write(**kwargs)

def delete_file(**kwargs):
    @app_storage(action='delete', **kwargs)
    def _delete(**kwargs):
        pass
    return _delete(**kwargs)