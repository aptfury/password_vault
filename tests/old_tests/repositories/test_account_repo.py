'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Unit test cases for AccountRepo
'''

import json
import pytest

from pathlib import Path
from datetime import datetime

from src.app.models import AccountModel, AccountAuthModel

def test_get_raw_data(tmp_path, account_repo):
    
    ### create data to fetch ###
    ### TODO: Work on a factory for generating user data ###
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / 'accounts.json'
    
    password: AccountAuthModel = AccountAuthModel(
        auth_salt='alskdjfalsdf',
        auth_hash='a_hashed_string_lol',
        vault_id=None,
        vault_salt=None
    )
    
    account: AccountModel = AccountModel(
        _id='1',
        name='oogabooga',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    with open(test_path, 'w', encoding='utf-8') as file:
        json.dump([account.model_dump(by_alias=True, mode='json')], file, indent=4)
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    res = repo.get_raw_data()
    assert AccountModel.model_validate(res[0]) == account

def test_create(tmp_path, account_repo):

    test_dir: Path = tmp_path / 'database'
    test_name: str = 'accounts'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / f'{test_name}.json'
    
    with open(test_path, 'w', encoding='utf-8') as file:
        file.write('[]')
    
    password: AccountAuthModel = AccountAuthModel(
        auth_salt='alskdjfalsdf',
        auth_hash='a_hashed_string_lol',
        vault_id=None,
        vault_salt=None
    )
    
    account: AccountModel = AccountModel(
        _id='1',
        name='oogabooga',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    created = repo.create(account)
    
    assert created
    
def test_get_all(tmp_path, account_repo):
    
    ### create data to fetch ###
    ### TODO: Work on a factory for generating user data ###
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / 'accounts.json'
    
    password: AccountAuthModel = AccountAuthModel(
        auth_salt='alskdjfalsdf',
        auth_hash='a_hashed_string_lol',
        vault_id=None,
        vault_salt=None
    )
    
    account: AccountModel = AccountModel(
        _id='1',
        name='oogabooga',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    with open(test_path, 'w', encoding='utf-8') as file:
        json.dump([account.model_dump(by_alias=True, mode='json')], file, indent=4)
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    accounts = repo.get_all()
    
    assert [isinstance(acc, AccountModel) for acc in accounts]
    
def test_get_id_and_get_by_id(tmp_path, account_repo):
    
    ### create data to fetch ###
    ### TODO: Work on a factory for generating user data ###
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / 'accounts.json'
    
    password: AccountAuthModel = AccountAuthModel(
        auth_salt='alskdjfalsdf',
        auth_hash='a_hashed_string_lol',
        vault_id=None,
        vault_salt=None
    )
    
    account: AccountModel = AccountModel(
        _id='1',
        name='oogabooga',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    with open(test_path, 'w', encoding='utf-8') as file:
        json.dump([account.model_dump(by_alias=True, mode='json')], file, indent=4)
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    id: str = repo.get_id(key='name', value='oogabooga')
    
    assert id == account.id
    
    res: AccountModel = repo.get_by_id(id)
    
    assert res == account
    
def test_get_one_where_get_all_where(tmp_path, account_repo):
    
    ### create data to fetch ###
    ### TODO: Work on a factory for generating user data ###
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / 'accounts.json'
    
    password: AccountAuthModel = AccountAuthModel(
        auth_salt='alskdjfalsdf',
        auth_hash='a_hashed_string_lol',
        vault_id=None,
        vault_salt=None
    )
    
    account_one: AccountModel = AccountModel(
        _id='1',
        name='oogabooga',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    account_two: AccountModel = AccountModel(
        _id='2',
        name='Lola',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    account_three: AccountModel = AccountModel(
        _id='3',
        name='alexx',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    test_accounts: list[AccountModel] = [account_one, account_two, account_three]
    
    with open(test_path, 'w', encoding='utf-8') as file:
        json.dump([account.model_dump(by_alias=True, mode='json') for account in test_accounts], file, indent=4)
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    user = repo.get_one_where(key='name', value='alexx')
    
    assert user == account_three
    
    # check that get_one_where does not pull more than one
    user = repo.get_one_where(key='email', value='blep@blep.com')
    
    assert isinstance(user, AccountModel)
    assert user == account_one
    
    # check get_all_where() w/o limit
    users = repo.get_all_where(key='email', value='blep@blep.com')
    
    assert [acc in users for acc in test_accounts]
    assert [isinstance(acc, AccountModel) for acc in users]
    
    # check get_all_where() w/ limit
    
    users = repo.get_all_where(key='email', value='blep@blep.com', limit=2)
    
    assert len(users) == 2
    assert len(users) == len(test_accounts) - 1
    assert [acc in test_accounts for acc in users]
    
def test_delete_methods(tmp_path, account_repo):
    
    ### create data to fetch ###
    ### TODO: Work on a factory for generating user data ###
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / 'accounts.json'
    
    password: AccountAuthModel = AccountAuthModel(
        auth_salt='alskdjfalsdf',
        auth_hash='a_hashed_string_lol',
        vault_id=None,
        vault_salt=None
    )
    
    account_one: AccountModel = AccountModel(
        _id='1',
        name='oogabooga',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    account_two: AccountModel = AccountModel(
        _id='2',
        name='Lola',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    account_three: AccountModel = AccountModel(
        _id='3',
        name='alexx',
        email='blep@blep.com',
        password=password,
        created=datetime.now()
    )
    
    test_accounts: list[AccountModel] = [account_one, account_two, account_three]
    
    with open(test_path, 'w', encoding='utf-8') as file:
        json.dump([account.model_dump(by_alias=True, mode='json') for account in test_accounts], file, indent=4)
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    deleted: bool = repo.delete_one_where('name', 'oogabooga')
    all_users: list[AccountModel] = repo.get_all()
    
    assert deleted
    assert not account_one in all_users
    
    # check errors
    with pytest.raises(LookupError) as lookup_error:
        repo.delete_one_where('name', 'vincent')
        assert lookup_error
    
    # delete_all_where()
    all_deleted: bool = repo.delete_all_where('email', 'blep@blep.com')
    all_users: list[AccountModel] = repo.get_all()
    
    assert all_deleted
    assert [user not in all_users for user in test_accounts]
    
    # check errors
    with pytest.raises(LookupError) as lookup_error:
        repo.delete_all_where('email', 'blep@blep.com')
        assert lookup_error
        
def test_delete_file(tmp_path, account_repo):
    
    ### create data to fetch ###
    ### TODO: Work on a factory for generating user data ###
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / 'accounts.json'
    
    with open(test_path, 'w', encoding='utf-8') as file:
        file.write('[]')
        
    repo = account_repo(is_test=True, test_dir=test_dir)
    deleted: bool = repo.delete_database()
    
    assert deleted
    assert not test_path.exists()
    assert test_dir.exists()