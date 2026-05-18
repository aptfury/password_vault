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
        
    # def test_login(self, auth):
    #     fake: Faker = Faker()
    #     service: AuthService = auth
        
    #     username: str = fake.user_name()
    #     raw_password: str = fake.password()
    #     email: str = fake.email()
        
    #     success: bool = service.create_user(username, raw_password, email)
        
    #     assert success
        
    #     success: bool = service.login(username, raw_password)
        
    #     assert service.session.session_key is not None
    #     assert service.session.id is not None
    #     assert service.session.username is not None