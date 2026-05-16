'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Mocks of the repositories.
'''

# ------------ imports ------------ #
import pytest
from unittest.mock import MagicMock
from src.app.repositories.account_repo import AccountRepo
from src.app.repositories.vault_repo import VaultRepo

# ------------ account ------------ #
@pytest.fixture
def mock_account_repo(mock_account_payload):
    mock = MagicMock(spec=AccountRepo)
    
    _, snapshot_one = mock_account_payload
    _, snapshot_two = mock_account_payload
    
    mock.create.return_value = True
    mock.get_all.return_value = [snapshot_one, snapshot_two]
    mock.get_id.return_value = snapshot_one.id
    mock.get_by_id.return_value = snapshot_one
    mock.get_one_where.return_value = snapshot_one
    mock.get_all_where.return_value = [snapshot_one, snapshot_two]
    mock.update_one_where.return_value = True
    mock.delete_one_where.return_value = True
    mock.delete_all_where.return_value = True
    mock.delete_database.return_value = True
    
    return mock

# ------------ vault ------------ #
@pytest.fixture
def mock_vault_repo(mock_vault_payload):
    mock = MagicMock(spec=VaultRepo)
    
    _, snapshot_one = mock_vault_payload
    _, snapshot_two = mock_vault_payload
    
    mock.create.return_value = True
    mock.get_all.return_value = [snapshot_one, snapshot_two]
    mock.get_id.return_value = snapshot_one.id
    mock.get_by_id.return_value = snapshot_one
    mock.get_one_where.return_value = snapshot_one
    mock.get_all_where.return_value = [snapshot_one, snapshot_two]
    mock.update_one_where.return_value = True
    mock.delete_one_where.return_value = True
    mock.delete_all_where.return_value = True
    mock.delete_database.return_value = True
    
    return mock
    
    
