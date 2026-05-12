'''
AUTHOR: Blake Lemarr
DATE: 05.12.26
DESCRIPTION: Security utilities for account and data management.
'''

# ------------ IMPORTS ------------ #
import os
import base64
import hashlib
import secrets

from dotenv import load_dotenv

from ..models import AccountAuthModel

# ------------ SET UP ------------ #
load_dotenv()

# ------------ SECURITY ------------ #
class HashUtils:
    def __init__(self):
        self.__ACCOUNT_PEPPER = os.getenv('ACCOUNT_PEPPER')
        self.__VAULT_PEPPER = os.getenv('VAULT_PEPPER')
        
    def __verify_peppers(self):
        if not self.__ACCOUNT_PEPPER:
            raise SystemError('No account pepper available.')
        
        if not self.__VAULT_PEPPER:
            raise SystemError('No vault pepper available.')
        
    def __generate_salt(self) -> bytes | str:
        salt_bytes: bytes = secrets.token_bytes(32)
        salt: str = base64.b64encode(salt_bytes).decode('utf-8')
        
        return salt_bytes, salt
        
    def _hash_password(self, raw_password: str, stored_auth: AccountAuthModel | None = None) -> AccountAuthModel:
        self.__verify_peppers() # verify active peppers
        
        # generate salts
        salt_bytes, salt = self.__generate_salt()
        
        # attach pepper
        peppered: str = raw_password + self.__ACCOUNT_PEPPER
        
        # encode peppered password
        peppered_bytes: bytes = peppered.encode('utf-8')
        
        # generate password hash
        hash_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            peppered_bytes,
            salt_bytes,
            600000
        )
        
        # convert hash to str
        hash_string: str = base64.b64encode(hash_bytes).decode('utf-8')
        
        if stored_auth is not None:
            return AccountAuthModel(
                auth_salt=salt,
                auth_hash=hash_string,
                vault_id=stored_auth.vault_id,
                vault_salt=stored_auth.vault_salt
            )
        else:
        
            # return account password
            return AccountAuthModel(
                auth_salt=salt,
                auth_hash=hash_string,
                vault_id=None,
                vault_salt=None
            )
        
    def _validate_hash(self, raw_password: str, stored_password: AccountAuthModel) -> bool:
        self.__verify_peppers() # verify active peppers
        
        # generate hash from raw password
        peppered: str = raw_password + self.__ACCOUNT_PEPPER
        peppered_bytes: bytes = peppered.encode('utf-8')
        salt_bytes: bytes = base64.b64decode(stored_password.auth_salt)
        hash_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            peppered_bytes,
            salt_bytes,
            600000
        )
        hash_string: str = base64.b64encode(hash_bytes).decode('utf-8')
        
        return secrets.compare_digest(hash_string, stored_password.auth_hash)
        