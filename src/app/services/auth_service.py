'''
AUTHOR: Blake Lemarr
DATE: 05.12.26
DESCRIPTION: Manages all the authorization for using the application
'''

# ------------ IMPORTS ------------ #
from pydantic import EmailStr
from datetime import datetime

from ..repositories import AccountRepo
from ..utilities import EncryptUtils, HashUtils, IdentUtils
from ..models import AccountModel, AccountAuthModel, VaultEntryModel, VaultModel

# ------------ AUTH SERVICE ------------ #
class AuthService:
    def __init__(self, account_repo: AccountRepo, encrypt_utils: EncryptUtils, hash_utils: HashUtils, ident_utils: IdentUtils):
        self.account_repo: AccountRepo = account_repo
        self.encrypt_utils: EncryptUtils = encrypt_utils
        self.hash_utils: HashUtils = hash_utils
        self.ident_utils: IdentUtils = ident_utils
        
    def create_account(self, name: str, raw_password: str, email: EmailStr) -> bool:
        # hash user password and create user auth model
        password: AccountAuthModel = self.hash_utils._hash_password(raw_password, None)
        
        # generate missing vault_id
        password.vault_id = self.ident_utils.generate_lookup_id()
        
        # create user account model
        user: AccountModel = AccountModel(
            _id=self.ident_utils.generate_secure_id(),
            name=name,
            email=email,
            password=password,
            created=datetime.now()
        )
        
        return self.account_repo.create(user)
    
    def login(self, name: str, raw_password: str) -> bool:
        # get user
        user: AccountModel = self.account_repo.get_one_where('name', name)
        
        # check raw_password vs. stored password
        valid_login: bool = self.hash_utils._validate_hash(raw_password=raw_password, stored_password=user.password)
        
        # login is valid, begin session
        if valid_login:
            session_key: bytes = self.hash_utils._generate_session_key(raw_password=raw_password, stored_password=user.password)
            
            # open session
            self.encrypt_utils.set_session_key(session_key)
            
        return valid_login
            
    def access_granted(self) -> bool:
        return self.encrypt_utils._fernet is not None
            
    def logout(self):
        self.encrypt_utils.lock()
