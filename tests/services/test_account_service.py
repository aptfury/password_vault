'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Test cases for account service
'''

# ------------ imports ------------ #
import pytest
from src.app.services.auth_service import AuthService
from src.app.services.account_service import AccountService

# ------------ class ------------ #
class TestAccountService:
    def test_logged_in(self, account_service, auth, generate_user):
        service: AccountService = account_service
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
            service: AccountService = account_service
            service.logged_in()
            assert exec_info
        
    def test_view_account(self, account_service, auth, generate_user, capsys):
        service: AccountService = account_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        auth.login(username, password)
        
        service.view_account()
        
        captured = capsys.readouterr()
        assert username in captured.out
        assert email in captured.out
        
    def test_update_account(self, account_service, auth, generate_user, capsys):
        service: AccountService = account_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        auth.login(username, password)
        
        bad_update: dict = {
            '_id': 'bad_id',
            'created': 'bad_created'
        }
        
        service.update_account(bad_update)
        
        captured = capsys.readouterr()
        
        assert 'User id cannot be changed.' in captured.out
        assert 'Account creation date cannot be changed.' in captured.out
        assert 'No changes were made, update cancelled.' in captured.out
        
        good_update: dict = {
            'username': 'not_fake_username'
        }
        
        service.update_account(good_update)
        
        captured = capsys.readouterr()
        
        assert 'UPDATE SUCCESSFUL!' in captured.out
        
    def test_delete_account(self, account_service, auth, generate_user):
        service: AccountService = account_service
        auth: AuthService = auth

        user: dict = generate_user()
        username: str = user['account'].username
        password: str = user['raw_password']
        email: str = user['account'].email
        
        auth.create_user(username, password, email)
        auth.login(username, password)
        
        deleted: bool = service.delete_account()
        
        assert deleted

        with pytest.raises(Exception) as exec_info:
            service.repo.get('_id', service.session.id)
            assert exec_info