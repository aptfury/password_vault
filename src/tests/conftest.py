import pytest
from pathlib import Path

from app.storage import StorageConfig, AppStorage
from app.repositories import AccountRepo
from app.utilities import IdentUtils, HashUtils

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