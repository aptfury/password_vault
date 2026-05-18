'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Controller for the entire system
'''

# ------------ imports ------------ #
import sys
from pathlib import Path
from .account_controller import AccountController
from .vault_controller import VaultController
from ..configs import Database
from ..services import AccountService, VaultService, AuthService, SessionService
from ..repositories import AccountRepo, VaultRepo
from ..utilities import ScriptsUtilities

# ------------ paths ------------ #
src_dir: Path = Path(__file__).resolve().parent.parent
db_dir: Path = src_dir / 'db'
account_dir: Path = db_dir / 'accounts.json'
vault_dir: Path = db_dir / 'vaults.json'

# ------------ class ------------ #
class SystemController:
    def __init__(self):
        # databases #
        self.account_database: Database = Database(db_path=account_dir)
        self.vault_database: Database = Database(db_path=vault_dir)
        
        # repos #
        self.account_repo: AccountRepo = AccountRepo(database=self.account_database)
        self.vault_repo: VaultRepo = VaultRepo(database=self.vault_database)
        
        # services #
        self.session: SessionService = SessionService()
        self.auth: AuthService = AuthService(session=self.session, account_repo=self.account_repo, vault_repo=self.vault_repo)
        self.account_service: AccountService = AccountService(session=self.session, auth=self.auth, repository=self.account_repo)
        self.vault_service: VaultService = VaultService(session=self.session, auth=self.auth, repository=self.vault_repo)
        
        # controllers #
        self.account_controller: AccountController = AccountController(session=self.session, auth=self.auth, service=self.account_service)
        self.vault_controller: VaultController = VaultController(session=self.session, auth=self.auth, service=self.vault_service)
        
        # utilities #
        self.scripts: ScriptsUtilities = ScriptsUtilities()
        
    def main_menu(self):
        """Guides the user through the main menu
        """        
        self.scripts.main_menu()
        
        nav: list = ['1', '2', '3']
        
        res: str = None
        
        for n in range(3):
            res = self.scripts.menu_option()
            
            if res in nav:
                break
            else:
                remaining: int = 3 - n
                print(f'[INVALID OPTION] {res} is not a valid menu option. (REMAINING ATTEMPTS: {remaining} of 3).')
                
                if remaining <= 0:
                    raise KeyError('[MAIN_CONTROLLER_NAV] 3 invalid menu options in a row')
                
        if res == '1':
            pass # create account
        if res == '2':
            pass # log in
        if res == '3':
            print('Goodbye!')
            sys.exit()
            
    def create_account(self):
        """Creates an account and vault for the user
        """        
        username: str = input('\nCREATE USERNAME: ')
        password: str = input('CREATE PASSWORD: ')
        email: str = input('(OPTIONAL) CREATE EMAIL: ')
        
        created: bool = self.auth.create_user(username, password, email)
        
        if created:
            print('Account created! Please log in to continue.')
        else:
            print('Account could not be created at this time.')
            
        self.main_menu()
        
    def log_in(self):
        """Logs into an account.
        """        
        username: str = input('\nUSERNAME: ')
        password: str = input('\nPASSWORD: ')
        
        logged_in: bool = self.auth.login(username, password)
        
        if logged_in:
            # todo - update to nav cycle
            self.account_controller.account_navigation()
        else:
            print('Incorrect username or password.')
            self.main_menu()
            
    def cycle_account(self):
        nav: str = self.account_controller.account_navigation()
        
        # to vaults #
        if nav == '1':
            self.cycle_vault()
        
        # log out #
        elif nav == '4':
            self.logout()
            
        # delete #
        elif nav == '9':
            self.delete()

    def cycle_vault(self):
        nav: str = self.vault_controller.vault_navigation()
        
        # to account #
        if nav == '5':
            self.cycle_account()
        
        # log out #
        elif nav == '6':
            self.logout()
        
        # delete #
        elif nav == '9':
            self.delete()
        

    def cycle_password(self):
        nav: str = self.vault_controller.password_navigation()
        
        # to accounts #
        self.cycle_account()
        
        # log out #
        self.logout()

    def logout(self):
        """Logs the user out
        """        
        if self.session.username is not None:
            print(f'Goodbye, {self.session.username}!')
            
        else:
            print('Goodbye!')
            
        self.auth.logout()
        self.main_menu()
    
    def delete(self):
        """Deletes the user account and vault.
        """        
        confirm: str = input('Type CONFIRM to verify account and vault deletion: ')
        
        if not confirm == 'CONFIRM':
            print('Account saved.')
            
            if self.auth.access_granted():
                self.cycle_account()
            else:
                self.main_menu()
                
        self.logout()
        self.vault_controller.delete_vault()
        self.account_controller.delete_account()
        self.main_menu()