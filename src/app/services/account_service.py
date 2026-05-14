'''
AUTHOR: Blake Lemarr
DATE: 05.13.26
DESCRIPTION: Manages all of the account operations for the application
'''

# ------------ IMPORTS ------------ #
import sys
import secrets

from getpass import getpass
from datetime import datetime
from pydantic import EmailStr
from input_with_timeout import input_with_timeout

from ..models import (
    AccountModel,
    AccountAuthModel,
    VaultEntryModel,
    VaultModel
)
from ..utilities import (
    EncryptUtils,
    HashUtils,
    IdentUtils
)
from .auth_service import AuthService
from ..repositories import AccountRepo

# ------------ ACCOUNT SERVICE ------------ #
class AccountService:
    def __init__(self):
        # ------ config ------ #
        self.repo: AccountRepo = AccountRepo()
        self.encrypt: EncryptUtils = EncryptUtils()
        self.hash: HashUtils = HashUtils()
        self.id: IdentUtils = IdentUtils()
        self.auth: AuthService = AuthService(
            account_repo=self.repo,
            encrypt_utils=self.encrypt,
            hash_utils=self.hash,
            ident_utils=self.id
        )
        
        # ------ user session ------ #
        self.session_id: str = None
        self.__id: str = None
        self.name: str = None
        
    def create_account(self) -> None:
        
        name: str = None
        raw_password: str = None
        email: EmailStr = None
        
        try:
            # TODO: Add in username exists check - account utils
            # TODO: Add in username valid check - account utils
            # USERNAME should be at least 2 chars and include only letters & digits
            name = input_with_timeout('Enter a username: ', timeout=10)
            
            if name is None or '':
                print('You must provide a name/username for the account.')
                name = input_with_timeout('Enter a username: ', timeout=10)
                
                if name is None or '':
                    print('Username was not accepted. Please try again later.')
                    sys.exit()
                    return
        except TimeoutError:
            print('Account creation timed out on username.')
            sys.exit()
            return
            
        try:
            # TODO: Add in password valid check - account utils - use strings module
            # PASSWORD should be at least 8 chars (1 upper, 1 lower, 1 digit, 1 punctuation)
            attempts: int = 1
            
            for attempts in range(3):
                raw_password: str = input_with_timeout(getpass('Enter a password: '), timeout=10)
                raw_password_again: str = input_with_timeout(getpass('Re-enter your password: '), timeout=10)
                
                is_match: bool = secrets.compare_digest(raw_password, raw_password_again)
                
                if not is_match:
                    print(f'\nPasswords did not match. Please try again. (Attempt: {attempts} of 3)\n')
                    attempts += 1
                    
                    if attempts >= 3:
                        print('No more password attempts available. Please try again later.')
                        sys.exit()
                        return
                else:
                    attempts = 1
                    break
        except TimeoutError:
            print('Account creation timed out on password.')
            sys.exit()
            return
            
        try:
            # TODO - Check valid email
            email: str = input_with_timeout('(OPTIONAL) Enter your email: ', timeout=10)
            
        except TimeoutError:
            print('Account creation timed out on email.')
            sys.exit()
            return
            
        created: bool = self.auth.create_account(name=name, raw_password=raw_password, email=email)
        
        if not created:
            print('Account creation failed. Please restart the program and try again.')
            sys.exit()
            return
        
        user: AccountModel = self.repo.get_one_where('name', name)
        
        if not user.name == name:
            # TODO: Eventually create a file to house error messages
            # TODO: Eventually create custom errors with codes based on file
            error_msg: str = f'''
            -------------------------------
                    ACCOUNT FAILURE
            -------------------------------
            
            Your account could not be created due to an internal system error.
            Please create an issue on the github to let the maintainer(s) know.
            
            Provide the following information:
            
                SYSTEM ERROR: ACCOUNT_CREATION_FAILURE
                WHERE: ACCOUNT_SERVICE
                WHY: CHECK_EXISTS_MISMATCH
                WHEN: {datetime.now()}
                
                DETAILS: {name} submitted, {user.name} saved
            '''
            
            raise SystemError(error_msg)
        