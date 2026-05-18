'''
AUTHOR: Blake Lemarr
DATE: 05.17.26
DESCRIPTION: Manages authorization actions for the system
'''

# ------------ imports ------------ #
from pydantic import EmailStr
from .session_service import SessionService
from ..utilities import SecurityUtilities
from ..repositories import AccountRepo, VaultRepo
from ..configs.models import AccountModel, PasswordModel, VaultModel

# ------------ class ------------ #
class AuthService:
    def __init__(self, session: SessionService):
        self.account: AccountRepo = AccountRepo()
        self.vault: VaultRepo = VaultRepo()
        self.session: SessionService = session
        self.utils: SecurityUtilities = SecurityUtilities()

    def create_user(self, username: str, raw_password: str, email: EmailStr) -> bool:
        # hash user password
        hashed_password: PasswordModel = self.utils.hash_password(raw_password=raw_password)
        
        #generate vault salt
        salt: str = self.utils.generate_vault_salt()
        
        # create account model
        user_account: AccountModel = AccountModel(
            username=username,
            email=email,
            password=hashed_password
        )
        
        # create vault model
        user_vault: VaultModel = VaultModel(
            _id=user_account.id,
            vault_salt=salt
        )
        
        # create account and vault
        # todo - create errors
        account_created: bool = self.account.create(user_account)
        vault_created: bool = self.vault.create(user_vault)
        
        return account_created and vault_created

    def login(self, username: str, raw_password: str) -> bool:
        # get user account
        user_account: AccountModel = self.account.get('username', username)
        user_vault: VaultModel = self.vault.get('_id', user_account.id)
        
        is_valid_login: bool = self.utils.validate_password(raw_password=raw_password, stored_password=user_account.password)
        
        if is_valid_login:
            session_key: bytes = self.utils.generate_session_key(raw_password=raw_password, vault_salt=user_vault.salt)
            
            self.utils.set_session_key(key=session_key)
            
            self.session.login(key=session_key, id=user_account.id, username=user_account.username)
            
        return is_valid_login
    
    def access_granted(self) -> bool:
        return self.session.session_key is not None
    
    def logout(self) -> bool:
        self.session.logout()
        self.utils.lock()
        
        return not self.access_granted()