'''
AUTHOR: Blake Lemarr
DATE: 05.17.26
DESCRIPTION: Test cases for auth service
'''

# ------------ imports ------------ #
from faker import Faker
from src.app.configs.models import AccountModel
from src.app.services.auth_service import AuthService

# ------------ class ------------ #
class TestAuthService:
    def test_create_user(self, auth, generate_user):
        service: AuthService = auth

        fake: Faker = Faker()
        raw_password: str = fake.password()
        user: dict = generate_user()
        
        success: bool = service.create_user(user['account'].username, raw_password, user['account'].email)
        
        assert success
        
        account: AccountModel = service.account.get('username', user['account'].username)
        
        assert account.username == user['account'].username
        assert account.email == user['account'].email
        
    def test_login(self, auth, generate_user):
        service: AuthService = auth

        fake: Faker = Faker()
        raw_password: str = fake.password()
        user: dict = generate_user()
        
        success: bool = service.create_user(user['account'].username, raw_password, user['account'].email)
        
        assert success
        
        logged_in: bool = service.login(user['account'].username, raw_password)
        account: AccountModel = service.account.get('username', user['account'].username)
        
        assert logged_in
        assert account.id == service.session.id
        assert service.utils.session_is_active()
        assert service.session.session_id is not None
        assert account.username == service.session.username
        
    def test_access_granted(self, auth, generate_user):
        service: AuthService = auth

        fake: Faker = Faker()
        raw_password: str = fake.password()
        user: dict = generate_user()
        
        success: bool = service.create_user(user['account'].username, raw_password, user['account'].email)
        
        assert success
        
        access_is_false: bool = service.access_granted()
        
        assert not access_is_false
        
        service.login(user['account'].username, raw_password)
        
        access_is_true: bool = service.access_granted()
        
        assert access_is_true
        
    def test_logout(self, auth, generate_user):
        service: AuthService = auth

        fake: Faker = Faker()
        raw_password: str = fake.password()
        user: dict = generate_user()
        
        success: bool = service.create_user(user['account'].username, raw_password, user['account'].email)
        
        assert success
        
        service.login(user['account'].username, raw_password)
        logged_out: bool = service.logout()
        
        assert logged_out
        assert service.session.id is None
        assert service.session.username is None
        assert service.session.session_id is None
        assert not service.utils.session_is_active()