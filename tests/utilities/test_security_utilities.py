'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Test case for security utils
'''

# ------------ imports ------------ #
from faker import Faker
from src.app.configs.models import VaultModel, EntryModel
from src.app.services.auth_service import AuthService

# ------------ class ------------ #
class TestSecurityUtilities:
    '''
    The following have already been tested between
    conftest, test_auth, and test_session:
        - __generate_salt()
        - hash_password()
        - generate_vault_salt()
        - validate_password()
        - generate_session_key()
        - set_session_key()
        - session_is_active()
        - lock()
        
    Only vault encryption and decryption need to be tested
    '''
    
    def test_encrypt_decrypt(self, auth, generate_user, generate_vault_entries):
        auth: AuthService = auth

        fake: Faker = Faker()
        raw_password: str = fake.password()
        
        user: dict = generate_user(raw_password)
        
        auth.create_user(user['account'].username, raw_password, user['account'].email)
        auth.login(user['account'].username, raw_password)
        
        assert auth.utils.session_is_active()
        
        id: str = auth.account.get_id('username', user['account'].username)
        vault: VaultModel = auth.vault.get('_id', id)
        
        for _ in range(15):
            entry: EntryModel = generate_vault_entries()
            vault.vault.append(entry)
            
        json_vault: str = vault.model_dump(by_alias=True, mode='json')
            
        encrypted_entries: bytes = auth.utils.encrypt_vault(json_vault['vault'])
        
        assert isinstance(encrypted_entries, bytes)
        
        decrypted_entries: list = auth.utils.decrypt_vault(encrypted_entries)
        json_vault['vault'] = decrypted_entries
        
        decrypted_vault: VaultModel = VaultModel.model_validate(json_vault)
        
        assert isinstance(decrypted_vault, VaultModel)
        assert vault == decrypted_vault
        
        for i in range(len(vault.vault)):
            assert vault.vault[i] == decrypted_vault.vault[i]
        