'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Frequent factories needed for the test suite.
'''

# ------------ imports & config ------------ #
import pytest
from faker import Faker
from app.utilities.hash_utils import HashUtils
from app.models.vault_models import VaultModel
from app.utilities.ident_utils import IdentUtils
from app.models.account_models import AccountModel
from app.models.vault_models import VaultEntryModel
from app.models.account_models import AccountAuthModel
from app.models.vault_models import VaultLoginDataModel
# ------------------------------------------ #

# ----------------- data factories ----------------- #
@pytest.fixture(scope='session', autouse=True)
def seed_faker():
    fake = Faker()
    fake.seed_instance(18)
    
@pytest.fixture
class AccountFactory:
    def __init__(self, **kwargs):
        self.fake = Faker()
        self.hash = HashUtils()
        self.ident = IdentUtils()
        self.id = self.ident.generate_secure_id() or kwargs.get('_id')
        self.name = self.fake.name() or kwargs.get('name')
        self.email = self.fake.email() or kwargs.get('email')
        self.raw_password = self.fake.password() or kwargs.get('raw_password')
        self.password: AccountAuthModel = self.hash._hash_password(self.raw_password, None)
        self.password.vault_id = self.ident.generate_lookup_id() or kwargs.get('vault_id')
        self.created = self.fake.date_time() or kwargs.get('created')
        
    def get(self, as_dict: bool = False):
        acc: AccountModel = AccountModel(
            _id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            created=self.created
        )
        
        if as_dict:
            return acc.model_dump(by_alias=True, mode='json')
        else:
            return acc
        
@pytest.fixture
class VaultFactory:
    def __init__(self, **kwargs):
        self.fake = Faker()
        self.account: AccountModel = AccountFactory(**kwargs).get() or kwargs.get('account')
        self.id = self.account.password.vault_id
        self.user_id = self.account.id
        self.created = self.fake.date_time()
        self.vault = []
        
    def get(self, as_dict: bool = False):
        vault: VaultModel = VaultModel(
            _id=self.id,
            user_id=self.user_id,
            created=self.created,
            vault=self.vault
        )
        
        if as_dict:
            return vault.model_dump(by_alias=True, mode='json')
        else:
            return vault
        
@pytest.fixture
class VaultEntryFactory:
    def __init__(self, **kwargs):
        self.fake = Faker()
        self.ident = IdentUtils()
        self.id = self.ident.generate_nano_id()
        self.name = self.fake.user_name() or kwargs.get('username') or kwargs.get('name')
        self.website = f'www.{self.fake.domain_name()}.com' or kwargs.get('website')
        self.username = self.fake.user_name() or kwargs.get('username')
        self.password = self.fake.password() or kwargs.get('password')
        self.created = self.fake.date_time() or kwargs.get('created')
        self.login = VaultLoginDataModel(
            username=self.username,
            password=self.password
        ) or kwargs.get('login')
        
    def get(self, as_dict: bool = False):
        entry: VaultEntryModel = VaultEntryModel(
            _id=self.id,
            name=self.name,
            website=self.website,
            login=self.login,
            created=self.created
        )
        
        if as_dict:
            return entry.model_dump(by_alias=True, mode='json')
        else:
            return entry
        
    def add_to_vault(self, vault: VaultModel, entry: VaultEntryModel = None):
        entry = entry or self.get()
        return vault.vault.append(entry)
    
    def remove_from_vault(self, vault: VaultModel, entry: VaultEntryModel):
        return vault.vault.remove(entry)
