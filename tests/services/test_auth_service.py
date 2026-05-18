'''
AUTHOR: Blake Lemarr
DATE: 05.17.26
DESCRIPTION: Test cases for auth service
'''

# ------------ imports ------------ #
from faker import Faker
from src.app.services.auth_service import AuthService

# ------------ class ------------ #
class TestAuthService:
    def test_create_user(self, auth):
        fake: Faker = Faker()
        service: AuthService = auth
        
        username: str = fake.user_name()
        raw_password: str = fake.password()
        email: str = fake.email()
        
        success: bool = service.create_user(username, raw_password, email)
        
        assert success