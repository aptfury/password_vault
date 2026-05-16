'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Frequent factories needed for the test suite.
'''

# ------------ imports & config ------------ #
import pytest
from faker import Faker
from src.app.utilities.hash_utils import HashUtils
from src.app.models.vault_models import VaultModel
from src.app.utilities.ident_utils import IdentUtils
from src.app.models.account_models import AccountModel
from src.app.models.vault_models import VaultEntryModel
from src.app.models.account_models import AccountAuthModel
from src.app.models.vault_models import VaultLoginDataModel
# ------------------------------------------ #

# ----------------- mock account ----------------- #
@pytest.fixture
def mock_account_payload(faker, mock_ident_utils):
    fake: Faker = faker
    hash: HashUtils = HashUtils()
    ident: IdentUtils = mock_ident_utils
    
    raw_password: str = fake.password()
    payload: AccountModel = AccountModel(
        _id=ident.generate_secure_id(),
        name=fake.user_name(),
        email=fake.email(),
        password=hash._hash_password(raw_password, None),
        created=faker.date_time()
    )
    payload.password.vault_id = ident.generate_lookup_id()
    
    payload_dump = payload.model_dump(by_alias=True, mode='json')
    snapshot = AccountModel.model_validate(payload_dump)
    
    return payload, snapshot

# ------------ mock auth ------------ #
@pytest.fixture
def mock_auth_payload(faker, mock_ident_utils):
    fake: Faker = faker
    hash: HashUtils = HashUtils()
    ident: IdentUtils = mock_ident_utils
    
    raw_password: str = fake.password()
    
    payload: AccountAuthModel = hash._hash_password(raw_password, None)
    payload.vault_id = ident.generate_lookup_id()
    
    payload_dump = payload.model_dump(by_alias=True, mode='json')
    snapshot = AccountAuthModel.model_validate(payload_dump)
    
    return payload, snapshot

# ------------ mock vault ------------ #
@pytest.fixture
def mock_vault_payload(faker, mock_ident_utils):
    fake: Faker = faker
    ident: IdentUtils = mock_ident_utils
    
    payload: VaultModel = VaultModel(
        _id=ident.generate_lookup_id(),
        user_id=ident.generate_secure_id(),
        created=fake.date_time(),
        vault=[]
    )
    
    payload_dump = payload.model_dump(by_alias=True, mode='json')
    snapshot = VaultModel.model_validate(payload_dump)
    
    return payload, snapshot

# ------------ mock entry ------------ #
@pytest.fixture
def mock_entry_payload(faker, mock_ident_utils):
    fake: Faker = faker
    ident: IdentUtils = mock_ident_utils
    
    payload: VaultEntryModel = VaultEntryModel(
        _id=ident.generate_nano_id(),
        name=fake.user_name(),
        website=fake.url(),
        login=VaultLoginDataModel(
            username=fake.user_name(),
            password=fake.password()
        ),
        created=fake.date_time()
    )
    
    payload_dump = payload.model_dump(by_alias=True, mode='json')
    snapshot = VaultEntryModel.model_validate(payload_dump)
    
    return payload, snapshot

# ------------ mock login ------------ #
@pytest.fixture
def mock_login_payload(faker):
    fake: Faker = faker

    payload: VaultLoginDataModel = VaultLoginDataModel(
        username=fake.user_name(),
        password=fake.password()
    )
    
    payload_dump = payload.model_dump(by_alias=True, mode='json')
    snapshot = VaultLoginDataModel.model_validate(payload_dump)
    
    return payload, snapshot