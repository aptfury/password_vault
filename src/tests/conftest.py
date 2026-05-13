import pytest
from pathlib import Path

from app.storage import StorageConfig, AppStorage
from app.repositories import AccountRepo
from app.utilities import IdentUtils, HashUtils, EncryptUtils
from app.services import AuthService

# ---------- storage_config ---------- #
@pytest.fixture
def storage_config(tmp_path):

    def _storage_config(**kwargs) -> StorageConfig:

        config_kwargs = {
            'is_test': True,
            'test_dir': tmp_path,
            'test_db_name': 'accounts',
            **kwargs
        }


        return StorageConfig(**config_kwargs)

    return _storage_config

# ---------- app_storage ---------- #
@pytest.fixture
def app_storage(tmp_path):
    def _app_storage(action: str, **kwargs) -> AppStorage:
        config_kwargs = {
            'is_test': True,
            'test_dir': tmp_path,
            'test_db_name': 'acconts',
            **kwargs
        }
        
        return AppStorage(action=action, **config_kwargs)
    return _app_storage

# ---------- account_repo ---------- #
@pytest.fixture
def account_repo(tmp_path) -> AccountRepo:
    def _account_repo(**kwargs) -> AccountRepo:
        config_kwargs = {
            'is_test': True,
            'test_dir': tmp_path / 'database',
            **kwargs
        }
        repo = AccountRepo(**config_kwargs)
        return repo
    return _account_repo

# ---------- ident_utils ---------- #
@pytest.fixture
def ident_utils() -> IdentUtils:
    def _ident_utils() -> IdentUtils:
        utils = IdentUtils()
        return utils
    return _ident_utils

# ---------- hash_utils ---------- #
@pytest.fixture
def hash_utils() -> HashUtils:
    def _hash_utils() -> HashUtils:
        utils = HashUtils()
        return utils
    return _hash_utils

# ---------- encrypt_utils ---------- #
@pytest.fixture
def encrypt_utils() -> EncryptUtils:
    def _encrypt_utils() -> EncryptUtils:
        utils = EncryptUtils()
        return utils
    return _encrypt_utils

# ------------ auth_service ----------- #
@pytest.fixture
def auth_service(
    tmp_path,
    account_repo,
    encrypt_utils,
    hash_utils,
    ident_utils
) -> AuthService:
    config_kwargs = {
        'is_test': True,
        'test_dir': tmp_path / 'database'
    }
    
    repo: AccountRepo = account_repo(**config_kwargs)
    encrypt: EncryptUtils = encrypt_utils()
    hash: HashUtils = hash_utils()
    ident: IdentUtils = ident_utils()
    
    service: AuthService = AuthService(
        repo,
        encrypt,
        hash,
        ident
    )
    
    return service