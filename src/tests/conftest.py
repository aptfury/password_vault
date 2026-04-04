'''
Name: Blake Lemarr
Updated: 04.04.2026
Description: Fixtures and other configurations for unit and integration tests.
'''

# ===== IMPORTS =====

import pytest
from app.models import *
from app.services import *
from app.utilities import *
from app.controllers import *
from unittest.mock import MagicMock

# ===================

# ===== STORAGE FIXTURES =====

@pytest.fixture
def storage(tmp_path):
    # create testing path
    test_dir = tmp_path / 'database'
    test_file = 'test.json'

    # init storage service
    service = StorageService(test_dir, test_file)

    # create the directory and json file
    service.create_if_missing()

    return service # return storage service instance

@pytest.fixture
def mock_storage(tmp_path):
    # directory
    mock_path = tmp_path / 'mock_storage.json'

    # create mock storage environment
    mock = MagicMock(spec=StorageService)
    mock_path.write_text('[]')

    # defaults
    mock.read_file.return_value = []
    mock.construct_path.return_value = mock_path
    mock.create_if_missing.return_value = True
    mock.full_path = mock_path

    return mock

# ============================

# ===== SERVICE FIXTURES =====

@pytest.fixture
def mock_account_service(mock_storage):
    service = AccountService(storage=mock_storage)

    return service

# ============================

# ===== MODEL FIXTURES =====

@pytest.fixture
def account_models():
    create = CreateAccount(
        username='test',
        password='belligerent',
        email='penelope@outmail.com',
    )
    password = AccountPassword(
        salt='something_something_salt',
        hash='something_something_hash',
    )
    internal = AccountInternal(
        username='pickles and cheese',
        pii_email='pickes@outmail.com',
        hashed_password=password,
    )
    public = AccountPublic
    status = AccountStatus

    return {
        'create': create,
        'internal': internal,
        'public': public,
        'status': status,
        'password': password
    }

# ==========================