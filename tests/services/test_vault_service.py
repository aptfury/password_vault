'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Test cases for vault service
'''

# ------------ imports ------------ #
import pytest
from src.app.configs.models import VaultModel, EntryModel
from src.app.services.auth_service import AuthService
from src.app.services.vault_service import VaultService

# ------------ class ------------ #
class TestVaultService:
    def test_logged_in(self, vault_service, auth, generate_user):
        service: VaultService = vault_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        auth.login(username, password)
        
        assert service.logged_in() is None
        
        auth.logout()
        
        with pytest.raises(PermissionError) as exec_info:
            service.logged_in()
            assert exec_info
            
    def test_add_password(self, vault_service, auth, generate_user, generate_vault_entries):
        service: VaultService = vault_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        
        new_password: EntryModel = generate_vault_entries()
        
        auth.login(username, password)
        
        updated: bool = service.add_password(new_password.website, new_password.username, new_password.password)
        
        assert updated
        
        vault: VaultModel = service.repo.get('_id', service.session.id)
        target: EntryModel = None
        
        for entry in vault.vault:
            if entry.username == new_password.username:
                target = entry

        assert target.website == new_password.website
        assert target.username == new_password.username
        
    def test_find_password(self, vault_service, auth, generate_user, generate_vault_entries):
        service: VaultService = vault_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        
        new_password: EntryModel = generate_vault_entries()
        
        auth.login(username, password)
        
        updated: bool = service.add_password(new_password.website, new_password.username, new_password.password)
        
        assert updated
        
        results: list = service.find_password('username', new_password.username)
        
        assert len(results) == 1
        assert results[0].website == new_password.website
        assert results[0].username == new_password.username
        
    def test_view_passwords(self, vault_service, auth, generate_user, generate_vault_entries):
        service: VaultService = vault_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        
        new_password: EntryModel = generate_vault_entries()
        new_password_two: EntryModel = generate_vault_entries()
        
        auth.login(username, password)
        
        updated: bool = service.add_password(new_password.website, new_password.username, new_password.password)
        updated_two: bool = service.add_password(new_password_two.website, new_password_two.username, new_password_two.password)
        
        assert updated and updated_two

        results: list[EntryModel] = service.view_passwords()
        
        assert len(results) == 2
        assert results[0].website == new_password.website
        assert results[0].username == new_password.username
        assert results[1].website == new_password_two.website
        assert results[1].username == new_password_two.username
        
    def test_edit_password(self, vault_service, auth, generate_user, generate_vault_entries):
        service: VaultService = vault_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        
        new_password: EntryModel = generate_vault_entries()
        
        auth.login(username, password)
        
        updated: bool = service.add_password(new_password.website, new_password.username, new_password.password)
        
        assert updated
        
        stored: list[EntryModel] = service.find_password('username', new_password.username)
        new: EntryModel = generate_vault_entries()
        
        pass_updated: bool = service.edit_password(stored[0].id, 'username', new.username)
        
        assert pass_updated

        stored: list[EntryModel] = service.find_password('id', stored[0].id)
        
        assert len(stored) == 1
        assert stored[0].website == new_password.website
        assert stored[0].username == new.username
        assert stored[0].password == new_password.password
        
    def test_delete_password(self, vault_service, auth, generate_user, generate_vault_entries):
        service: VaultService = vault_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        
        new_password: EntryModel = generate_vault_entries()
        
        auth.login(username, password)
        
        updated: bool = service.add_password(new_password.website, new_password.username, new_password.password)
        
        assert updated
        
        stored: EntryModel = service.find_password('username', new_password.username)[0]
        
        deleted: bool = service.delete_password(stored.id)
        
        results: list[EntryModel] = service.view_passwords()
        
        assert deleted
        assert results == []
        
    def test_delete_all_passwords(self, vault_service, auth, generate_user, generate_vault_entries):
        service: VaultService = vault_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        
        new_password: EntryModel = generate_vault_entries()
        
        auth.login(username, password)
        
        updated: bool = service.add_password(new_password.website, new_password.username, new_password.password)
        
        assert updated
        
        deleted: bool = service.delete_all_passwords()
        results: list[EntryModel] = service.view_passwords()
        
        assert deleted
        assert results == []
        
    def test_delete_vault(self, vault_service, auth, generate_user, generate_vault_entries):
        service: VaultService = vault_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        
        new_password: EntryModel = generate_vault_entries()
        
        auth.login(username, password)
        
        deleted: bool = service.delete_vault()
        
        assert deleted
        
        with pytest.raises(Exception) as exec_info:
            vault: VaultModel = service.repo.get('_id', service.session.id)
            assert exec_info