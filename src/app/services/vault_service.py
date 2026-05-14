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
        self.vault_id: str = None
        
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
        if self.auth.access_granted:
            user: AccountModel = self.acc_repo.get_one_where('name', name)
            self.vault_id = user.password.vault_id
        else:
            raise PermissionError('ACCESS_FORBIDDEN: If this is an error, please close the application and log in again.')
        
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
        
        print(menu_options)
        nav_choice: int = int(input('\nWhat would you like to do? Enter the number: '))
        
        if nav_choice == 1:
            self.add_password()
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
        
    def add_password(self) -> bool:
        
        entry: VaultEntryModel = VaultEntryModel(
            _id=self.id.generate_nano_id(),
            name='',
            website='',
            login=VaultLoginDataModel(
                username='',
                password=''
            ),
            created=str(datetime.now())
        )
        
        entry.name = input('(Optional - Enter to skip)\nPassword Name: ')
        
        entry.website = input('(Optional - Enter to skip)\nWebsite: ')
        
        entry.login.username = input('(Optional = Enter to skip)\nUsername: ')
        
        entry.login.password = input('Password: ')

        if entry.login.password == '':
            print('[ALERT!] You must enter a password.')
            
            entry.login.password = input('Password: ')
            
            if entry.login.password == '':
                raise ValueError('No password entered; Action aborted.')
                    
        print('You can edit the password any time. Here is the entry ID - it can be used to find the password later, so be sure to save it somewhere safe.')
        print(f'\n#### PASSWORD ID: {entry.id} ####\n')
        
        vault: VaultModel = self.repo.get_by_id(self.vault_id)
        vault.vault.append(entry)
        
        saved: bool = self.repo.update_one_where(vault, '_id', self.vault_id)
        
        if saved:
            print('Password added to vault!')
            print(f'PASSWORD ENTRY: {json.dumps(entry.model_dump(by_alias=True, mode='json'), indent=4)}')
            return saved
        else:
            raise SystemError('Password could not be saved. Please try again later.')
        
    
            
