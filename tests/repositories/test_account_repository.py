'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Test cases for the account repository
'''

# ------------ imports ------------ #
from src.app.configs.models import AccountModel
from src.app.repositories.account_repository import AccountRepo

# ------------ class ------------ #
class TestAccountRepository:
    def test_create(self, account_repo, generate_user):
        user = generate_user()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['account'])
        
        assert success

    def test_get(self, account_repo, generate_user):
        user  = generate_user()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['account'])
        
        assert success
        
        res: AccountModel = repo.get('username', user['account'].username)
        
        assert user['account'] == res
        
    def test_get_id(self, account_repo, generate_user):
        user  = generate_user()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['account'])
        
        assert success
        
        res: str = repo.get_id('username', user['account'].username)
        
        assert user['account'].id == res
        
    def test_update(self, account_repo, generate_user):
        user  = generate_user()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['account'])
        
        assert success
        
        user_two = generate_user()
        user_two['account'].id = user['account'].id
        user_two['account'].email = user['account'].email
        user_two['account'].password = user['account'].password
        user_two['account'].created = user['account'].created

        success: bool = repo.update('_id', user['account'].id, user_two['account'])
        
        assert success

    def test_delete(self, account_repo, generate_user):
        user = generate_user()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(user['account'])
        
        assert success
        
        success: bool = repo.delete('username', user['account'].username)
        
        assert success