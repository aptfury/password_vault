'''
AUTHOR: Blake Lemarr
DATE: 05.12.26
DESCRIPTION: Encryption utilities for vault protection
'''

# ------------ IMPORTS ------------ #
import json

from dotenv import load_dotenv

from cryptography.fernet import Fernet

# ------------ SET UP ------------ #
load_dotenv()

# ------------ ENCRYPTION ------------ #
class EncryptUtils:
    def __init__(self):
        self._fernet = None

    def set_session_key(self, fernet_key: bytes):
        self.__fernet = Fernet(fernet_key)
        
    def encrypt_vault(self, data: list | dict) -> bytes:
        if not self.__fernet:
            raise PermissionError('You do not have a valid session key. Try signing in again.')
        
        json_data = json.dumps(data).encode('utf-8')
        
        return self._fernet.encrypt(json_data)
    
    def decrypt_vault(self, encrypted_blob: bytes) -> list | dict:
        if not self._fernet:
            raise PermissionError('You do not have a valid session key. Try signing in again.')
        
        decrypted_bytes = self._fernet.decrypt(encrypted_blob)
        return json.loads(decrypted_bytes.decode('utf-8'))
    
    def lock(self):
        self._fernet = None