'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Pytest configuration file
'''

# ---------- pytest config ---------- #
pytest_plugins = [
    'tests.mockeries.mock_models',
    'tests.mockeries.mock_utilities',
    'tests.mockeries.mock_repositories',
    'tests.mockeries.mock_storage'
]

# ---------- imports ---------- #
import json
import pytest
from faker import Faker
from pathlib import Path
from src.app.storage import StorageConfig
from src.app.repositories import AccountRepo, VaultRepo
from src.app.utilities import IdentUtils, HashUtils, EncryptUtils
from src.app.services import AuthService, AccountService, VaultService
from src.app.models import VaultEntryModel, VaultLoginDataModel

# ---------- faker config ---------- #
@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return 182

# ---------- tmp_file config ---------- #
@pytest.fixture
def file_config(tmp_path):
    src_dir: Path = tmp_path / 'database'
    src_dir.mkdir(parents=True, exist_ok=True)
    
    account_path: Path = src_dir / 'accounts.json'
    vault_path: Path = src_dir / 'vaults.json'
    
    with open(account_path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4)
        
    with open(vault_path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4)
        
    return account_path, vault_path

# ---------- storage_config ---------- #
@pytest.fixture
def storage_config(tmp_path, monkeypatch):
    def _storage_config(db_name: str, db_dir: str = 'database') -> StorageConfig:
        storage = StorageConfig(db_name, db_dir)
        test_path: Path = tmp_path / db_dir / f'{db_name}.json'
        test_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(test_path, 'w', encoding='utf-8') as file:
            json.dump([], file, indent=4)
            
        monkeypatch.setattr(storage, 'path', test_path)

        return storage
    return _storage_config

# # ---------- app_storage ---------- #
# @pytest.fixture
# def app_storage(tmp_path):
#     def _app_storage(action: str, **kwargs) -> AppStorage:
#         config_kwargs = {
#             'is_test': True,
#             'test_dir': tmp_path,
#             'test_db_name': 'acconts',
#             **kwargs
#         }
        
#         return AppStorage(action=action, **config_kwargs)
#     return _app_storage

# # ---------- account_repo ---------- #
# @pytest.fixture
# def account_repo(tmp_path) -> AccountRepo:
#     def _account_repo(**kwargs) -> AccountRepo:
#         config_kwargs = {
#             'is_test': True,
#             'test_dir': tmp_path / 'database',
#             **kwargs
#         }
#         repo = AccountRepo(**config_kwargs)
#         return repo
#     return _account_repo

# # ------------ vault_repo ------------#
# @pytest.fixture
# def vault_repo(tmp_path) -> VaultRepo:
#     def _vault_repo(**kwargs):
#         config_kwargs = {
#             'is_test': True,
#             'test_dir': tmp_path / 'database',
#             **kwargs
#         }
#         repo = VaultRepo(**config_kwargs)
#         return repo
#     return _vault_repo

# # ---------- ident_utils ---------- #
# @pytest.fixture
# def ident_utils() -> IdentUtils:
#     def _ident_utils() -> IdentUtils:
#         utils = IdentUtils()
#         return utils
#     return _ident_utils

# # ---------- hash_utils ---------- #
# @pytest.fixture
# def hash_utils() -> HashUtils:
#     def _hash_utils() -> HashUtils:
#         utils = HashUtils()
#         return utils
#     return _hash_utils

# # ---------- encrypt_utils ---------- #
# @pytest.fixture
# def encrypt_utils() -> EncryptUtils:
#     def _encrypt_utils() -> EncryptUtils:
#         utils = EncryptUtils()
#         return utils
#     return _encrypt_utils

# # ------------ auth_service ----------- #
# @pytest.fixture
# def auth_service(
#     tmp_path,
#     account_repo,
#     encrypt_utils,
#     hash_utils,
#     ident_utils
# ) -> AuthService:
#     config_kwargs = {
#         'is_test': True,
#         'test_dir': tmp_path / 'database'
#     }
    
#     repo: AccountRepo = account_repo(**config_kwargs)
#     encrypt: EncryptUtils = encrypt_utils()
#     hash: HashUtils = hash_utils()
#     ident: IdentUtils = ident_utils()
    
#     service: AuthService = AuthService(
#         repo,
#         encrypt,
#         hash,
#         ident
#     )
    
#     return service

# # ------------ account_service ------------ #
# @pytest.fixture
# def account_service(auth_service) -> AccountService:
#     service: AccountService = AccountService()
    
#     service.auth = auth_service
#     service.repo = auth_service.account_repo
#     service.encrypt = auth_service.encrypt_utils
#     service.hash = auth_service.hash_utils
#     service.id = auth_service.ident_utils
    
#     return service

# # ------------ vault_service ------------ #
# @pytest.fixture
# def vault_service(
#     tmp_path,
#     auth_service,
#     vault_repo,
#     **kwargs
# ) -> VaultService:
#     config_kwargs = {
#         'is_test': True,
#         'test_dir': tmp_path / 'database',
#         **kwargs
#     }
#     service: VaultService = VaultService()
    
#     service.repo = vault_repo(**config_kwargs)
#     service.auth = auth_service
#     service.acc_repo = auth_service.account_repo
#     service.encrypt = auth_service.encrypt_utils
#     service.hash = auth_service.hash_utils
#     service.id = auth_service.ident_utils
    
#     return service

# # ------------ account_factory ------------ #
# @pytest.fixture
# def account_factory(auth_service):
#     def _account_factory():
#         fake: Faker = Faker()
        
#         name: str = fake.user_name()
#         raw_password: str = fake.password()
#         email: str = fake.email()
        
#         created = auth_service.create_account(name, raw_password, email)
        
#         if created:
#             user = auth_service.account_repo.get_one_where('name', name)
#             return user, raw_password
#     return _account_factory

# @pytest.fixture
# def vault_entry_factory(ident_utils) -> VaultEntryModel:
#     def _vault_entry_factory() -> VaultEntryModel:
#         fake: Faker = Faker()
#         ident: IdentUtils = ident_utils()
        
#         login: VaultLoginDataModel = VaultLoginDataModel(
#             username=fake.user_name(),
#             password=fake.password()
#         )
        
#         entry: VaultEntryModel = VaultEntryModel(
#             _id=ident.generate_nano_id(),
#             name=fake.user_name(),
#             website=f'https://www.{fake.user_name()}{fake.domain_name()}',
#             login=login,
#             created=str(fake.date_time_this_month())
#         )
        
#         return entry
    
#     return _vault_entry_factory
