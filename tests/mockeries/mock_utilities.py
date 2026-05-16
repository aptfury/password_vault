'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Global mocks of system-heavy static utilities.
'''

# ------------ imports ------------ #
import pytest
from faker import Faker
from cryptography.fernet import Fernet
from src.app.utilities.ident_utils import IdentUtils
from src.app.utilities.encrypt_utils import EncryptUtils

# ------------ mock ident_utils ------------ #
@pytest.fixture
def mock_ident_utils(mocker) -> IdentUtils:
    utils: IdentUtils = IdentUtils()
    
    id_types: list[str] = ['secure', 'lookup', 'trace', 'nano']
    
    def sequential_id(type: str) -> str:
        return (f'ID_{type.upper()}_{i}' for i in range(1, 1000))
    
    for type in id_types:
        seq_id: str = sequential_id(type)
        
        mocker.patch.object(utils, f'generate_{type}_id', side_effect=seq_id)
        
    mocker.patch.object(utils, 'verify_uuid', return_value=True)
    mocker.patch.object(utils, 'verify_trace_id', return_value=True)
    mocker.patch.object(utils, 'verify_nano_id', return_value=True)
    
    return utils
        
# ------------ mock encrypt_utils ------------ #
@pytest.fixture
def mock_encrypt_utils() -> EncryptUtils:
    utils: EncryptUtils = EncryptUtils()
    
    key = Fernet.generate_key()
    utils.set_session_key(key)
    
    return utils
    
    