from app.models import *

def test_create(account_service, account_factory):
    for _ in range(5):
        user = account_factory()
        created = account_service.create(user)
        assert created and created is not None

def test_query_user(account_service, account_factory):
    for _ in range(5):
        user = account_factory()

        created = account_service.create(user)
        assert created and created is not None

        query_username = account_service.query_user('username', user.username)
        assert query_username == user

        query_email = account_service.query_user('pii_email', user.pii_email)
        assert query_email == user

def test_query_users(account_service, account_factory):
    created_users: list[AccountInternal] = [account_factory(username='jonah') for _ in range(5)]
    assert [isinstance(user, AccountInternal) for user in created_users]
    assert len(created_users) == 5

    created: list[bool] = [account_service.create(new_user) for new_user in created_users]
    assert [created for user in created]
    assert len(created) == len(created_users)

    users: list[AccountInternal] = [account_service.query_users('username', user.username) for user in created_users]
    assert len(users) == len(created_users)