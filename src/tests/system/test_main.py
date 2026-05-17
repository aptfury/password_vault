'''
AUTHOR: Blake Lemarr
DATE: 05.17.26
DESCRIPTION: Test cases for the main file
'''

# ------------ imports ------------ #
import json
# import pytest
from pathlib import Path
from app.main import main

# ------------ tests ------------ #
class TestMain:
    def test_does_launch(self, tmp_path, hash_utils, ident_utils, encrypt_utils, auth_service, account_service, vault_service, monkeypatch):
        test_dir: Path = tmp_path / 'database'
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_vaults: Path = test_dir / 'vaults.json'
        test_accounts: Path = test_dir / 'accounts.json'
        
        with open(test_accounts, 'w', encoding='utf-8') as file:
            json.dump([], file, indent=4)
            
        with open(test_vaults, 'w', encoding='utf-8') as file:
            json.dump([], file, indent=4)
            
        monkeypatch.setattr(main, 'hash_utils', hash_utils)
        monkeypatch.setattr(main, 'ident_utils', ident_utils)
        monkeypatch.setattr(main, 'encrypt_utils', encrypt_utils)
        
        monkeypatch.setattr(main, 'auth_service', auth_service)
        
        monkeypatch.setattr(main, 'vaults', vault_service)
        monkeypatch.setattr(main, 'accounts', account_service)
        
        welcome_message = '''
------------------------------------------
        WELCOME TO PASSWORD VAULT!    
------------------------------------------
Select an option to get started:

(1) Create Account
(2) Log In
(3) Exit
'''
