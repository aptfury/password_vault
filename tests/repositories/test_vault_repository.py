'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Test cases for the vault repo
'''

# ------------ imports ------------ #
from src.app.configs.models import VaultModel
from src.app.repositories.vault_repository import VaultRepo

# ------------ class ------------ #
class TestVaultRepository:
    def test_create(self, vault_repo, generate_user):
        user = generate_user()
        repo: VaultRepo = vault_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['vault'])
        
        assert success
        
    def test_get(self, vault_repo, generate_user):
        user = generate_user()
        repo: VaultRepo = vault_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['vault'])
        
        assert success

        res: VaultModel = repo.get('_id', user['vault'].id)
        
        assert user['vault'] == res
        
    def test_get_id(self, vault_repo, generate_user):
        user = generate_user()
        repo: VaultRepo = vault_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['vault'])
        
        assert success
        
        res: str = repo.get_id('_id', user['vault'].id)
        
        assert res == user['vault'].id
        
    def test_update(self, vault_repo, generate_user):
        user = generate_user()
        repo: VaultRepo = vault_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['vault'])
        
        assert success
        
        user_two = generate_user()
        
        success: bool = repo.update('_id', user['vault'].id, user_two['vault'])
        
        assert success
        
    def test_delete(self, vault_repo, generate_user):
        user = generate_user()
        repo: VaultRepo = vault_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['vault'])
        
        assert success
        
        success: bool = repo.delete('_id', user['vault'].id)
        
        assert success
