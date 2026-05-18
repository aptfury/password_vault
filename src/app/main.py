'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: The main script.
'''

# ------------ imports ------------ #
from pathlib import Path
from .configs import Database
from .repositories import AccountRepo, VaultRepo
from .services import AuthService, SessionService

# ------------ configs ------------ #
def database_setup(name: str) -> Database:
    """Creates a json database based on the name provided.

    Args:
        name (str): The name of the database file

    Returns:
        database (Database): The database
    """    
    # verifies the path of the current file - DO NOT CHANGE
    src_dir: Path = Path(__file__).resolve().parent
    
    # verifies the json file name will be correct
    database_name: str = name if name.endswith('.json') else f'{name}.json'
    
    # this is the directory/folder where the database files are saved
    db_dir: Path = src_dir / 'db'
    
    # this is the database file where data is saved
    database_path: Path = db_dir / database_name
    
    # this is the accounts database
    database: Database = Database(db_path=database_path)
    
    return database


session: SessionService = SessionService()
auth: AuthService = AuthService(session=session)
vault_database: Database = database_setup('vaults')
account_database: Database = database_setup('accounts')
vault_repo: VaultRepo = VaultRepo(database=vault_database)
account_repo: AccountRepo = AccountRepo(database=account_database)

# ------------ main program ------------ #
def main():
    pass

main()