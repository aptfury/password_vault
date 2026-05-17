'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Config file for tests
'''

# ------------ imports ------------ #
import pytest
from uuid import uuid4
from faker import Faker
from pathlib import Path
from src.app.configs.database import Database
from src.app.repositories.vault_repository import VaultRepo
from src.app.repositories.account_repository import AccountRepo
from src.app.configs.models import AccountModel, PasswordModel, VaultModel, EntryModel

# ------------ configs ------------ #
pytest_plugins = [
    'tests.mockeries.mock_database'
]

# ------------ fixtures ------------ #
@pytest.fixture
def tmp_database(tmp_path) -> Database:
    test_path: Path = tmp_path / 'accounts.json'
    database: Database = Database(db_path=test_path)
    return database

# ------------ account_repo ------------ #
@pytest.fixture
def account_repo(tmp_database, monkeypatch) -> AccountRepo:
    repo: AccountRepo = AccountRepo()
    
    monkeypatch.setattr(repo, 'db', tmp_database)
    return repo

@pytest.fixture
def vault_repo(tmp_database, monkeypatch) -> VaultRepo:
    repo: VaultRepo = VaultRepo()
    
    monkeypatch.setattr(repo, 'db', tmp_database)
    return repo

# ------------ vault faker ------------ #
@pytest.fixture
def gen_vault() -> VaultModel:
    def _gen_vault() -> VaultModel:
        fake: Faker = Faker()
        vault: VaultModel = VaultModel(
            _id=fake.uuid4(),
            vault=[]
        )
        return vault
    return _gen_vault