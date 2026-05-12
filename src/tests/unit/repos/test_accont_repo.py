'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Unit test cases for AccountRepo
'''

import json

from pathlib import Path
from datetime import datetime

from app.models import AccountModel, AccountPasswordModel
from app.repos import AccountRepo

def test_get_raw_data(tmp_path, account_repo):
    
    ### create data to fetch ###
    ### TODO: Work on a factory for generating user data ###
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / 'accounts.json'
    
    password: AccountPasswordModel = AccountPasswordModel(
        salt='alskdjfalsdf',
        hash='a_hashed_string_lol'
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
    
    password: AccountPasswordModel = AccountPasswordModel(
        salt='alskdjfalsdf',
        hash='a_hashed_string_lol'
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
    
    password: AccountPasswordModel = AccountPasswordModel(
        salt='alskdjfalsdf',
        hash='a_hashed_string_lol'
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
    
def test_get_id(tmp_path, account_repo):
    
    ### create data to fetch ###
    ### TODO: Work on a factory for generating user data ###
    test_dir: Path = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path: Path = test_dir / 'accounts.json'
    
    password: AccountPasswordModel = AccountPasswordModel(
        salt='alskdjfalsdf',
        hash='a_hashed_string_lol'
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
