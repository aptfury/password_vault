'''
AUTHOR: Blake Lemarr
DATE: 05.12.26
DESCRIPTION: Unit testing suite for hashing utils
'''

from app.models import AccountAuthModel

def test_hash_utils(hash_utils):
    raw_password = 'asldkfjwoei#@lakjfsd23509'
    
    util = hash_utils()
    
    existing_auth: AccountAuthModel = AccountAuthModel(
        auth_salt='nah',
        auth_hash='also nah',
        vault_id='notreally',
        vault_salt='idkman'
    )
    
    new_auth: AccountAuthModel = util._hash_password(raw_password, existing_auth)
    
    assert not new_auth.auth_salt == existing_auth.auth_salt
    assert not new_auth.auth_hash == existing_auth.auth_hash
    assert new_auth.vault_id == existing_auth.vault_id
    assert new_auth.vault_salt == existing_auth.vault_salt
    
    new_auth = util._hash_password(raw_password)
    
    assert new_auth.auth_salt is not None
    assert new_auth.auth_hash is not None
    assert new_auth.vault_id is None
    assert new_auth.vault_salt is None
    
    new_auth = util._hash_password(raw_password, existing_auth)
    
    login: bool = util._validate_hash(raw_password, new_auth)
    
    assert login