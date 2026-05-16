'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Holds the mocked instances of StorageConfig and AppStorage
'''

# ------------ imports ------------ #
import pytest
from faker import Faker
from unittest.mock import MagicMock
from src.app.storage.storage_config import StorageConfig
from src.app.storage.app_storage import AppStorage

# ------------ mock config ------------ #
@pytest.fixture
def mock_storage(tmp_path, monkeypatch):
    # def _mock_storage(db_name: str):
    #     storage: StorageConfig = StorageConfig(db_name=db_name)
    #     mock = MagicMock(wraps=StorageConfig)
    #     path = tmp_path / 'database' / f'{db_name}.json'
        
    #     storage.path = path
        
    #     monkeypatch.setattr(StorageConfig, mock)
        
    #     return mock
    original_init = StorageConfig.__init__

    def mock_init(self, db_name: str, db_dir: str = 'database'):
        original_init(self, db_name, db_dir)
        self.path = tmp_path / db_dir / f'{db_name}.json'
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
    monkeypatch.setattr(StorageConfig, '__init__', mock_init)
        