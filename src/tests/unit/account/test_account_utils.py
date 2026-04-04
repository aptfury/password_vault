from app.models import *

def test_create(account_util, account_service, util_account_factory):
    util = account_util
    service = account_service
    new_user: CreateAccount = util_account_factory()

    assert isinstance(new_user, CreateAccount)

    created: bool = util.create(new_user)
    assert created and created is not None

    account: AccountInternal = service.query_user(util.fields.username, new_user.username)
    assert isinstance(account, AccountInternal)
    assert account.username == new_user.username
    assert account.pii_email == new_user.email