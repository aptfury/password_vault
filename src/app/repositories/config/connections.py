'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Creates database connections.
'''

# ------------ imports ------------ #
from ...storage import AppStorage as app_storage

# ------------ accounts ------------ #
# @app_storage(action='read', db_name='accounts')
def read_accounts():
    pass

# @app_storage(action='add', db_name='accounts')
def add_account(data: str):
    pass

# @app_storage(action='update', db_name='accounts')
def update_account(key: str, value: str, data: str):
    pass

# @app_storage(action='delete', db_name='accounts')
def delete_account(key: str, value: str):
    pass

# ------------ vaults ------------ #
# @app_storage(action='read', db_name='vaults')
def read_vaults():
    pass

# @app_storage(action='add', db_name='vaults')
def add_vault(data: str):
    pass

# @app_storage(action='update', db_name='vaults')
def update_vault(key: str, value: str, data: str):
    pass

# @app_storage(action='delete', db_name='vaults')
def delete_vault(key: str, value: str):
    pass