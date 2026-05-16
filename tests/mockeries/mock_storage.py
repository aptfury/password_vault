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
def mock_storage_config(tmp_path, monkeypatch):
    config: StorageConfig = StorageConfig()
    mock = MagicMock(wraps=config)
    
    def path_builder(*args, **kwargs):
        return tmp_path / mock._db_dir / f'{mock._db_name}.json'

    mock._validate_data.return_value = True
    mock._build_path.side_effect = path_builder
    
    monkeypatch.setattr('src.app.storage.storage_config', mock)
    
    return mock
    
# ------------ mock app ------------ #
@pytest.fixture
def mock_app_storage(monkeypatch, mock_storage_config):
    
    def inherit_parent_path(self, *args, **kwargs):
        mock_storage_config._db_name = self._db_name
        self._build_path = mock_storage_config._build_path()
        return self._build_path
    
    monkeypatch.setattr(AppStorage, '_build_path', inherit_parent_path)
    monkeypatch.setattr(AppStorage, '_validate_data', lambda *args, **kwargs: True)