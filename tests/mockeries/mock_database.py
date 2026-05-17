'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: A mocked database for unit testing
'''

# ------------ imports ------------ #
import pytest
from pathlib import Path
from unittest.mock import MagicMock
from src.app.configs.database import Database

# ------------ class ------------ #
@pytest.fixture
def mock_database(tmp_path) -> Database:
    def _mock_database(file: str, data: list[dict]) -> Database:
        test_path: Path = tmp_path / file
        
        mock: Database = MagicMock(spec=Database)
        mock.db_path = test_path
        mock.initialized.return_value = True
        mock.read.return_value = data
        mock.add.return_value = True
        mock.update.return_value = True
        mock.delete.return_value = True
        
        return mock
    return _mock_database