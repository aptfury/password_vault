'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Config file for tests
'''

# ------------ imports ------------ #
import pytest
from faker import Faker
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock
from src.app.configs.database import Database
from src.app.repositories.vault_repository import VaultRepo
from src.app.repositories.account_repository import AccountRepo
from src.app.configs.models import AccountModel, PasswordModel, VaultModel, EntryModel
from src.app.services.session_service import SessionService
from src.app.services.auth_service import AuthService
from src.app.utilities.security_utilities import SecurityUtilities

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

# ------------ account repo ------------ #
@pytest.fixture
def account_repo(tmp_database) -> AccountRepo:
    repo: AccountRepo = AccountRepo(database=tmp_database)

    return repo

@pytest.fixture
def vault_repo(tmp_database) -> VaultRepo:
    repo: VaultRepo = VaultRepo(database=tmp_database)

    return repo

# ------------ vault faker ------------ #
@pytest.fixture
def generate_user(security) -> VaultModel:
    def _generate_user() -> VaultModel:
        fake: Faker = Faker()
        account: AccountModel = AccountModel(
            username=fake.user_name(),
            email=fake.email(),
            password=security.hash_password(fake.password())
        )
        vault: VaultModel = VaultModel(
            _id=account.id,
            salt=security.generate_vault_salt(),
            vault=[]
        )
        
        return account, vault
    
    return _generate_user

# ------------ security utilities ------------ #
@pytest.fixture
def security() -> SecurityUtilities:
    security: SecurityUtilities = SecurityUtilities()
    
    return security

# ----------- session service ------------ #
@pytest.fixture
def session() -> SessionService:
    session: SessionService = SessionService()
    
    return session

# ------------ auth service ------------ #
@pytest.fixture
def auth(session, account_repo, vault_repo, security, monkeypatch) -> AuthService:
    auth: AuthService = AuthService(session=session, account_repo=account_repo, vault_repo=vault_repo)
    monkeypatch.setattr(auth, 'utils', security)

    return auth