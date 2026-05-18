'''
AUTHOR: Blake Lemarr
DATE: 05.17.26
DESCRIPTION: Utilities for managing securities
'''

# ------------ imports ------------ #
import json
import base64
import hashlib
import secrets

from cryptography.fernet import Fernet
from ..configs.models import PasswordModel

# ------------ class ------------ #
class SecurityUtilities:
    def __init__(self):
        self.__fernet = None

    def __generate_salt(self) -> bytes | str:
        salt_bytes: bytes = secrets.token_bytes(32)
        salt: str = base64.b64encode(salt_bytes).decode('utf-8')
        
        return salt_bytes, salt

    def hash_password(self, raw_password: str) -> PasswordModel:
        salt_bytes, salt = self.__generate_salt()
        
        password_bytes: bytes = raw_password.encode('utf-8')
        
        password_hash_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt_bytes,
            600000
        )
        
        password_hash: str = base64.b64encode(password_hash_bytes).decode('utf-8')
        
        return PasswordModel(
            salt=salt,
            hashed=password_hash
        )

    def generate_vault_salt(self) -> str:
        _, salt = self.__generate_salt()
        
        return salt

    def validate_password(self, raw_password: str, stored_password: PasswordModel) -> bool:
        salt: str = stored_password.salt
        salt_bytes: bytes = base64.b64decode(salt.encode('utf-8'))
        
        password_bytes: bytes = raw_password.encode('utf-8')
        
        hash_bytes: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt_bytes,
            600000
        )
        
        hash_string: str = base64.b64encode(hash_bytes).decode('utf-8')
        
        return secrets.compare_digest(hash_string, stored_password.hashed)

    def generate_session_key(self, raw_password: str, vault_salt: str) -> bytes:
        password_bytes: bytes = raw_password.encode('utf-8')
        vault_salt_bytes: bytes = base64.b64decode(vault_salt.encode('utf-8'))
        
        raw_key: bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            vault_salt_bytes,
            600000
        )
        
        key: bytes = base64.b64encode(raw_key).decode('utf-8')
        
        return key

    def set_session_key(self, key: bytes):
        self.__fernet = Fernet(key)
        
        return

    def encrypt_vault(self, data: list) -> bytes:
        json_data: bytes = json.dumps(data).encode('utf-8')
        encrypted_vault: bytes = self.__fernet.encrypt(json_data)
        
        return encrypted_vault

    def decrypt_vault(self, data_bytes: bytes) -> list:
        decrypted_bytes: bytes = self.__fernet.decrypt(data_bytes)
        vault_data: str = decrypted_bytes.decode('utf-8')
        vault: list = json.loads(vault_data)
        
        return vault

    def lock(self):
        self.__fernet = None
        
        return