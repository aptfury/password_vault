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
    def test_create(self, account_repo, gen_account):
        account: AccountModel = gen_account()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(account)
        
        assert success

    def test_get(self, account_repo, gen_account):
        account: AccountModel = gen_account()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(account)
        
        assert success
        
        res: AccountModel = repo.get('username', account.username)
        
        assert account == res
        
    def test_get_id(self, account_repo, gen_account):
        account: AccountModel = gen_account()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(account)
        
        assert success
        
        res: str = repo.get_id('username', account.username)
        
        assert account.id == res
        
    def test_update(self, account_repo, gen_account):
        account: AccountModel = gen_account()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(account)
        
        assert success
        
        account_two: AccountModel = gen_account()
        account_two.id = account.id
        account_two.email = account.email
        account_two.password = account.password
        account_two.created = account.created

        success: bool = repo.update('_id', account.id, account_two)
        
        assert success

    def test_delete(self, account_repo, gen_account):
        account: AccountModel = gen_account()
        repo: AccountRepo = account_repo
        repo.db.initialized()
        
        success: bool = repo.create(account)
        
        assert success
        
        success: bool = repo.delete('username', account.username)
        
        assert success