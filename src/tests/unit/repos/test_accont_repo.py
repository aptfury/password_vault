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
        json.dump([account.model_dump(mode='json')], file, indent=4)
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    res = repo.get_raw_data()
    assert AccountModel.model_validate(res[0]) == account

def test_create(tmp_path, account_repo):

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
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    created = repo.create(account)
    
    assert created