'''
AUTHOR: Blake Lemarr
DATE: 05.12.26
DESCRIPTION: Test case for encryption utilities
'''

import pytest

from app.models import AccountAuthModel

def test_encrypt_utils(encrypt_utils, hash_utils):
    h_util = hash_utils()
    e_util = encrypt_utils()
    
    random_info: list[dict] = [
        {
            'dog': 'Lola',
            'species': 'Rat Terrier'
        },
        {
            'dog': 'Candy',
            'species': 'Lab Pittie'
        }
    ]
    
    account_auth: AccountAuthModel = h_util._hash_password('password')
    session_key = h_util._generate_session_key('password', account_auth)
    print(session_key)
    
    e_util.set_session_key(session_key)
    
    encrypted_data = e_util.encrypt_vault(random_info)
    print(encrypted_data)
    
    decrypted_data = e_util.decrypt_vault(encrypted_data)
    print(decrypted_data)
    
    assert decrypted_data == random_info
    
    e_util.lock()
    
    with pytest.raises(PermissionError) as perm_error:
        e_util.encrypt_vault(random_info)
        assert perm_error

        e_util.decrypt_vault(encrypted_data)
        assert perm_error
