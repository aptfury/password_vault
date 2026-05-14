'''
AUTHOR: Blake Lemarr
DATE: 05.14.26
DESCRIPTION: Manages all of the vault operations for the application.
'''

# ------------ IMPORTS ------------ #
import sys
import json
import secrets

# from getpass import getpass
from datetime import datetime
# from input_with_timeout import input_with_timeout

from ..models import AccountModel, AccountAuthModel, VaultModel, VaultEntryModel, VaultLoginDataModel

from ..repositories.vault_repo import VaultRepo
from ..repositories.account_repo import AccountRepo

from .auth_service import AuthService
from ..utilities import EncryptUtils, HashUtils, IdentUtils

# ------------ VAULT SERVICE ------------ #
class VaultService:
    def __init__(self):
    # ------ config ------ #
        self.repo: VaultRepo = VaultRepo()
        self.acc_repo: AccountRepo = AccountRepo()
        self.encrypt: EncryptUtils = EncryptUtils()
        self.hash: HashUtils = HashUtils()
        self.id: IdentUtils = IdentUtils()
        self.auth: AuthService = AuthService(
            account_repo=self.acc_repo,
            encrypt_utils=self.encrypt,
            hash_utils=self.hash,
            ident_utils=self.id
        )
        
        # ------ user session ------ #
        # self.session_id: str = None
        # self._id: str = None
        # self.name: str = None
        
    def create_vault(self, user: AccountModel) -> None:
        vault = VaultModel(
            _id=user.password.vault_id,
            user_id=user.id,
            created=str(datetime.now()),
            vault=[]
        )
        
        try:
            created = self.repo.create(vault)
            if created:
                return
            else:
                raise SystemError(f'An error occured and the vault could not be created at this time. (USER_ID: {user.id} | VAULT_ID: {user.password.vault_id})')
        except Exception as e:
            print(e)
            
    def vault_menu(self, name: str) -> str | None:
        menu_options: str = f'''
        Start Menu > Main Menu > Vault Menu
        {name}'s Password Vault
        
                VAULT MENU
            ------------------
        (1) Add Password
        (2) Find Password
        (3) View Passwords
        (4) Manage Passwords
        (5) Log Out / Exit
        '''
        
        nav_choice: int = int(input('What would you like to do? Enter the number: '))
        
        if nav_choice == 1:
            print('In production!')
        elif nav_choice == 2:
            print('In production!')
        elif nav_choice == 3:
            print('In production!')
        elif nav_choice == 4:
            print('In production!')
        elif nav_choice == 5:
            return 'log out'
        else:
            print('Invalid selection')
            return