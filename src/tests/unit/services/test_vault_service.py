'''
AUTHOR: Blake Lemarr
DATE: 05.14.26
DESCRIPTION: Test cases for vault service
'''

# ------------ IMPORTS ------------ #
import json
# import pytest
# todo - create pytest.raises() error checks

from faker import Faker
from pathlib import Path
from app.models import VaultModel, VaultEntryModel, VaultLoginDataModel

fake: Faker = Faker()

# ------------ VAULT SERVICE TEST ------------ #
def test_vault_service(monkeypatch, tmp_path, vault_service, account_factory, vault_entry_factory):
    # ------ start database config ------ #
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    accounts_path: Path = test_dir / 'accounts.json'
    vault_path: Path = test_dir / 'vaults.json'
    
    with open(accounts_path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4)
        
    with open(vault_path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4)
    # ------  end database config  ------ #
    
    # ------ start create vault ------ #
    service = vault_service
    user, raw_password = account_factory()
    logged_in: bool = service.auth.login(name=user.name, raw_password=raw_password)
    
    assert logged_in
    
    service.create_vault(user=user)
    vault: VaultModel = service.repo.get_one_where('user_id', user.id)
    
    assert vault.id == user.password.vault_id
    assert vault.user_id == user.id
    assert vault.vault == []
    # ------  end create vault  ------ #
    
    # ------ start add_password() ------ #
    fake_entry: VaultEntryModel = vault_entry_factory()
    add_pass_full_responses = iter([
        # '1',
        fake_entry.name,
        fake_entry.website,
        fake_entry.login.username,
        fake_entry.login.password
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(add_pass_full_responses))
    
    service.vault_menu(user.name)
    saved_new_password: bool = service.add_password()
    
    assert saved_new_password
    
    vault: VaultModel = service.repo.get_one_where('user_id', user.id)
    assert vault.vault[0].name in fake_entry
    # ------  end add_password()  ------ #