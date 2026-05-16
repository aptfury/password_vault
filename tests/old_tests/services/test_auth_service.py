'''
AUTHOR: Blake Lemarr
DATE: 05.12.26
DESCRIPTION: Test case for the authorization services
'''

import json

from pydantic import EmailStr

from src.app.models import AccountModel, AccountAuthModel

def test_auth_service(tmp_path, auth_service):
    tmp_dir = tmp_path / 'database'
    tmp_dir.mkdir(parents=True, exist_ok=True)
    test_db = tmp_dir / 'accounts.json'
    
    with open(test_db, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4)
        
    raw_name: str = 'Alexx'
    raw_password: str = 'lola&candy'
    raw_email: EmailStr = 'alexxandherdogs@google.com'
    
    auth_service.create_account(raw_name, raw_password, raw_email)
    
    data: list = []
    
    with open(test_db, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    user: AccountModel = AccountModel.model_validate(data[0])
    
    assert user.name == raw_name
    assert user.email == raw_email
    
    logged_in: bool = auth_service.login(name=raw_name, raw_password=raw_password)
    
    assert logged_in
    
    has_access: bool = auth_service.access_granted()
    
    assert has_access
    
    auth_service.logout()
    
    access_locked: bool = auth_service.access_granted()
    
    assert not access_locked