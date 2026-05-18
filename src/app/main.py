'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: The main script.
'''

# ------------ imports ------------ #
import sys
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
vault_database: Database = database_setup('vaults')
account_database: Database = database_setup('accounts')
vault_repo: VaultRepo = VaultRepo(database=vault_database)
account_repo: AccountRepo = AccountRepo(database=account_database)
auth: AuthService = AuthService(session=session, account_repo=account_repo, vault_repo=vault_repo)

# ------------ main program ------------ #
def main():
    greeting: str = '''
Welcome to Password Vault!

Choose from the menu options below:

(1) Create Account
(2) Log In
(3) Exit    
'''
    print(greeting)
    option: str = input('MENU OPTION (1, 2, 3):')
    
    if option == '1':
        print('Create account is in the works!')
    elif option == '2':
        print('Log in is in the worrks!')
    elif option == '3':
        print('Thank you for visiting!')
        sys.exit()
    else:
        raise ValueError(f'{option} is not an available menu option.')
    
if __name__ == '__main__':
    main()