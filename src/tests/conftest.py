import pytest
from pathlib import Path

from app.storage import StorageConfig, AppStorage

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