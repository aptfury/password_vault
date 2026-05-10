import pytest
from faker import Faker
from pathlib import Path

from app.storage import StorageConfig

# fake: Faker = Faker()

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