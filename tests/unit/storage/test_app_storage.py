'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Test cases for storage.
'''

# ------------ imports ------------- #
import json
from pathlib import Path
from src.app.models.account_models import AccountModel
from src.app.models.vault_models import VaultModel
from src.app.storage.storage_config import StorageConfig
from src.app.repositories.config.connections import (
    read_accounts,
    read_vaults,
    add_account,
    add_vault,
    update_account,
    update_vault,
    delete_account,
    delete_vault
)

# ------------ test cases ------------ #
class TestAppStorage:
    def test_paths_match(self, tmp_path, file_config):
        account: Path = file_config[0]
        vault: Path = file_config[1]
        
        assert account == tmp_path / 'database' / 'accounts.json'
        assert vault == tmp_path / 'database' / 'vaults.json'
        
    def test_create_and_read_account_with_path(self, file_config, mock_account_payload):
        account, _ = file_config

        payload, snapshot = mock_account_payload

        payload_dump = payload.model_dump(by_alias=True, mode='json')
        
        with open(account, 'w', encoding='utf-8') as file:
            json.dump([payload_dump], file, indent=4)
            
        raw_data = None

        with open(account, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)
            
        assert AccountModel.model_validate(raw_data[0]) == snapshot
        
    def test_create_and_read_vault_with_path(self, file_config, mock_vault_payload):
        _, vault = file_config

        payload, snapshot = mock_vault_payload
        
        payload_dump = payload.model_dump(by_alias=True, mode='json')
        
        with open(vault, 'w', encoding='utf-8') as file:
            json.dump([payload_dump], file, indent=4)
            
        raw_data = None
        
        with open(vault, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)
            
        assert VaultModel.model_validate(raw_data[0]) == snapshot
        
    def test_read_account(self, file_config, mock_account_payload, storage_config):
        account: Path = file_config[0]
        account.parent.mkdir(parents=True, exist_ok=True)
        storage: StorageConfig = storage_config('accounts', 'database')
        
        payload, snapshot = mock_account_payload
        
        payload_dump = payload.model_dump(by_alias=True, mode='json')
        
        storage.add(payload_dump)
            
        
        raw_data: list[dict] = storage.read()
            
        read_payload = AccountModel.model_validate(raw_data)
        
        assert read_payload == snapshot
        