'''
AUTHOR: Blake Lemarr
DATE: 05.17.26
DESCRIPTION: Test cases for session service
'''

# ------------ imports ------------ #
from faker import Faker
from src.app.services.auth_service import AuthService
from src.app.services.session_service import SessionService

# ------------ class ------------ #
class TestSessionService:
    def test_login(self, auth, session, generate_user):
        auth: AuthService = auth
        session: SessionService = session
        
        fake: Faker = Faker()
        raw_password: str = fake.password()
        user: dict = generate_user(raw_password)
        
        auth.create_user(user['account'].username, raw_password, user['account'].email)
        id: str = auth.account.get_id('username', user['account'].username)
        salt: str = auth.vault.get('_id', id).salt
        key: str = auth.utils.generate_session_key(raw_password, salt)
        
        session.login(key, id, user['account'].username)
        
        assert session.session_id == key
        assert session.id == id
        assert session.username == user['account'].username
        
    def test_logout(self, auth, session, generate_user):
        auth: AuthService = auth
        session: SessionService = session
        
        fake: Faker = Faker()
        raw_password: str = fake.password()
        user: dict = generate_user(raw_password)
        
        auth.create_user(user['account'].username, raw_password, user['account'].email)
        id: str = auth.account.get_id('username', user['account'].username)
        salt: str = auth.vault.get('_id', id).salt
        key: str = auth.utils.generate_session_key(raw_password, salt)
        
        session.login(key, id, user['account'].username)
        session.logout()
        
        assert session.session_id is None
        assert session.id is None
        assert session.username is None
