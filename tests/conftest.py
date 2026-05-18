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
from src.app.services.vault_service import VaultService
from src.app.services.account_service import AccountService
from src.app.utilities.security_utilities import SecurityUtilities
from src.app.controllers.account_controller import AccountController
from src.app.controllers.vault_controller import VaultController
from src.app.controllers.system_controller import SystemController

# ------------ configs ------------ #
pytest_plugins = [
    'tests.mockeries.mock_database'
]

# ------------ database ------------ #
@pytest.fixture
def account_database(tmp_path) -> Database:
    test_path: Path = tmp_path / 'accounts.json'
    database: Database = Database(db_path=test_path)
    
    return database

@pytest.fixture
def vault_database(tmp_path) -> Database:
    test_path: Path = tmp_path / 'vaults.json'
    database: Database = Database(db_path=test_path)
    
    return database

# ------------ account repo ------------ #
@pytest.fixture
def account_repo(account_database) -> AccountRepo:
    repo: AccountRepo = AccountRepo(database=account_database)

    return repo

@pytest.fixture
def vault_repo(vault_database) -> VaultRepo:
    repo: VaultRepo = VaultRepo(database=vault_database)

    return repo

# ------------ vault faker ------------ #
@pytest.fixture
def generate_user(security) -> VaultModel:
    def _generate_user(password: str = None) -> VaultModel:
        fake: Faker = Faker()
        raw_password: str = password if password is not None else fake.password()
        account: AccountModel = AccountModel(
            username=fake.user_name(),
            email=fake.email(),
            password=security.hash_password(raw_password)
        )
        vault: VaultModel = VaultModel(
            _id=account.id,
            salt=security.generate_vault_salt(),
            vault=[]
        )
        
        return {
            'account': account,
            'vault': vault,
            'raw_password': raw_password
        }
    
    return _generate_user

# ------------ entry faker ------------ #
@pytest.fixture
def generate_vault_entries() -> EntryModel:
    def _generate_vault_entries() -> EntryModel:
        fake: Faker = Faker()
        entry: EntryModel = EntryModel(
            website=fake.url(),
            username=fake.user_name(),
            _password=fake.password()
        )
        return entry
    return _generate_vault_entries

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
def auth(session, account_repo, vault_repo) -> AuthService:
    auth: AuthService = AuthService(session=session, account_repo=account_repo, vault_repo=vault_repo)

    return auth

# ------------ account service ------------ #
@pytest.fixture
def account_service(session, auth, account_repo):
    service: AccountService = AccountService(session, auth, account_repo)
    
    return service

# ------------ vault service ------------ #
@pytest.fixture
def vault_service(session, auth, vault_repo):
    service: VaultService = VaultService(session, auth, vault_repo)
    
    return service

# ------------ account controller ------------ #
@pytest.fixture
def account_controller(session, auth, account_service) -> AccountController:
    ctrl: AccountController = AccountController(session, auth, account_service)
    return ctrl

# ------------ vault controller ------------ #
@pytest.fixture
def vault_controller(session, auth, vault_service) -> VaultController:
    ctrl: VaultController = VaultController(session, auth, vault_service)
    return ctrl

# ------------ system controller ------------- #
@pytest.fixture()
def system_controller(session, auth, account_repo, vault_repo, account_service, vault_service, account_controller, vault_controller, account_database, vault_database, monkeypatch) -> SystemController:
    ctrl: SystemController = SystemController()
    
    monkeypatch.setattr(ctrl, 'session', session)
    monkeypatch.setattr(ctrl, 'auth', auth)
    monkeypatch.setattr(ctrl, 'account_repo', account_repo)
    monkeypatch.setattr(ctrl, 'vault_repo', vault_repo)
    monkeypatch.setattr(ctrl, 'account_service', account_service)
    monkeypatch.setattr(ctrl, 'vault_service', vault_service)
    monkeypatch.setattr(ctrl, 'account_controller', account_controller)
    monkeypatch.setattr(ctrl, 'vault_controller', vault_controller)
    monkeypatch.setattr(ctrl, 'account_database', account_database)
    monkeypatch.setattr(ctrl, 'vault_database', vault_database)
    
    return ctrl