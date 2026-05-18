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
    repo: AccountRepo = AccountRepo()
    repo.db = tmp_database

    return repo

@pytest.fixture
def vault_repo(tmp_database) -> VaultRepo:
    repo: VaultRepo = VaultRepo()
    repo.db = tmp_database

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

# ------------ account faker ------------ #
@pytest.fixture
def gen_account() -> AccountModel:
    def _account_vault() -> AccountModel:
        fake: Faker = Faker()
        account: AccountModel = AccountModel(
            _id=fake.uuid4(),
            username=fake.user_name(),
            email=fake.email(),
            password=PasswordModel(
                salt=str(fake.random_letters(18)),
                hashed=fake.password()
            ),
            created=datetime.now()
        )
        
        return account
    
    return _account_vault

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
def auth(session, account_repo, vault_repo, security) -> AuthService:
    auth: AuthService = AuthService(session=session)
    auth.account = account_repo
    auth.vault = vault_repo
    auth.utils = security

    return auth