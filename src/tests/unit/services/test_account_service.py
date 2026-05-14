'''
AUTHOR: Blake Lemarr
DATE: 05.13.26
DESCRIPTION: Test case for account service
'''

# ------------ IMPORTS ------------ #
import json

from pydantic import EmailStr
from app.models import AccountModel

# ------------ ACOUNT SERVICE TESTS ------------ #
def test_account_service(tmp_path, account_service, account_repo):
    test_dir = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path = test_dir / 'accounts.json'
    
    with open(test_path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent='4')
        
    # TODO - Add in monkeypatch for testing
    
    # NOTE - Until monkey patch, run pytest with -s --capture=no

    account_service.create_account()
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    
    user: AccountModel = repo.get_one_where('name', 'ThisName')
    
    assert user.name == 'ThisName'
    assert user.email == 'this@email.com'