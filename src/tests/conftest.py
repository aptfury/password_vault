import pytest
from faker import Faker
from src.app.storage import StorageConfig


fake: Faker = Faker()

# ---------- storage_config ---------- #
@pytest.fixture
def storage_config(tmp_path) -> StorageConfig:
    def _storage_config() -> StorageConfig:
        # other args should come from subclass & functions
        return StorageConfig(is_test=True, test_dir=tmp_path)
    return _storage_config()