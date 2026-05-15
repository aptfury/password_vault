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
from datetime import datetime
from app.models import VaultModel, VaultEntryModel, VaultLoginDataModel

fake: Faker = Faker()

# ------------ VAULT SERVICE TEST ------------ #
def test_vault_service(monkeypatch, tmp_path, vault_service, account_factory, vault_entry_factory, capsys):
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
    pass_id: str = ''
    
    add_pass = iter([
        '1',
        str(fake_entry.name),
        str(fake_entry.website),
        str(fake_entry.login.username),
        str(fake_entry.login.password),
        '1',
        'buchstabien',
        str(fake_entry.website),
        str(fake_entry.login.username),
        str(fake_entry.login.password),
        '2',
        'Name',
        'buchstabien',
        'n',
        '3',
        'n',
        '3',
        'y'
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(add_pass))
    
    service.vault_menu(user.name)
    
    vault: VaultModel = service.repo.get_one_where('user_id', user.id)
    assert vault.vault[0].name == fake_entry.name
    # ------  end add_password()  ------ #
    
    # ------ start find_password() ------ #
    service.vault_menu(user.name)
    service.vault_menu(user.name)
    
    captured = capsys.readouterr()
    
    assert 'RESULTS: 1 of 1' in captured.out
    # ------  end find_password()  ------ #
    
    # ------ start view_passwords() ------ #
    service.vault_menu(user.name)
    
    captured = capsys.readouterr()
    assert 'RESULTS: 1 of 2' in captured.out
    assert '*' in captured.out

    service.vault_menu(user.name)
    
    captured = capsys.readouterr()
    assert 'RESULTS: 2 of 2' in captured.out
    # ------  end view_passwords()  ------ #
    
    # ------ start edit_password() ------ #
    new_vault_entry: VaultEntryModel = VaultEntryModel(
        _id=service.id.generate_nano_id(),
        name='lolaandservicedogs',
        website='https://lolaandservicedogs.com',
        login=VaultLoginDataModel(
            username='lola',
            password='LolaAndCandy'
        ),
        created=str(datetime.now())
    )
    vault.vault.append(new_vault_entry)
    service.repo.update_one_where(vault, 'user_id', user.id)
    
    edit_pass = iter(['1', new_vault_entry.id, 'lola', '', '', '', 'y'])
    monkeypatch.setattr('builtins.input', lambda _: next(edit_pass))
    
    service.manage_passwords()
    
    captured = capsys.readouterr()
    assert 'CHANGES' in captured.out
    assert 'name: lola' in captured.out
    assert f'id: {new_vault_entry.id}' in captured.out
    # ------  end edit_password()  ------ #