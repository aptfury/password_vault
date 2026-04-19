import pytest

from app.models import *

def test_check_access_forbidden(account_util, mock_accounts):
    # INIT #
    util, storage_factory = account_util
    mocked_accounts = mock_accounts()

    storage_factory.enable_auto_sync()
    storage_factory.load_multi_mixed_accounts()

    custom_admin = mocked_accounts.create_account(status=AccountStatus.ADMIN)
    custom_user = mocked_accounts.create_account(status=AccountStatus.USER)
    custom_on_hold = mocked_accounts.create_account(status=AccountStatus.ON_HOLD)
    custom_banned = mocked_accounts.create_account(status=AccountStatus.BANNED)

    storage_factory.save_accounts([custom_admin, custom_user, custom_on_hold, custom_banned])
    storage_factory.build()

    # TEST LOGIC #
    admin_not_forbidden = util._check_access_forbidden(custom_admin)
    user_not_forbidden = util._check_access_forbidden(custom_user)

    with pytest.raises(PermissionError) as on_hold_is_forbidden:
        util._check_access_forbidden(custom_on_hold)

    with pytest.raises(PermissionError) as banned_is_forbidden:
        util._check_access_forbidden(custom_banned)

    # ASSERTIONS #
    assert admin_not_forbidden is None
    assert user_not_forbidden is None

    assert f'You cannot complete this operation while your account is {custom_on_hold.status}.' in str(on_hold_is_forbidden.value)

    assert f'You cannot complete this operation while your account is {custom_banned.status}.' in str(banned_is_forbidden.value)

def test_is_admin(account_util, mock_accounts):
    # INIT #
    util, storage_factory = account_util
    mocked_accounts = mock_accounts()

    storage_factory.enable_auto_sync()
    storage_factory.load_multi_mixed_accounts()

    custom_admin = mocked_accounts.create_account(status=AccountStatus.ADMIN)
    custom_user = mocked_accounts.create_account(status=AccountStatus.USER)
    custom_on_hold = mocked_accounts.create_account(status=AccountStatus.ON_HOLD)
    custom_banned = mocked_accounts.create_account(status=AccountStatus.BANNED)

    storage_factory.save_accounts([custom_admin, custom_user, custom_on_hold, custom_banned])
    storage_factory.build()

    # TEST LOGIC #
    account_is_admin = util._is_admin(custom_admin)
    account_is_user = util._is_admin(custom_user)
    account_is_on_hold = util._is_admin(custom_on_hold)
    account_banned = util._is_admin(custom_banned)

    # ASSERTIONS #
    assert account_is_admin
    assert not account_is_user
    assert not account_is_on_hold
    assert not account_banned

def test_create(account_util, mock_accounts):
    # INIT #
    util, storage_factory = account_util
    mocked_accounts = mock_accounts()

    storage_factory.enable_auto_sync()
    storage_factory.load_multi_mixed_accounts()
    storage_factory.build()

    # TEST LOGIC #
    new_user = mocked_accounts.create_sign_up()
    created = util.create(new_user)

    query_user = storage_factory.query_seeded_data('username', new_user.username)

    expected_username = query_user[0].username
    expected_email = query_user[0].pii_email

    # ASSERTIONS #
    assert created
    assert new_user.username == expected_username
    assert new_user.email == expected_email

def test_read_self(account_util, mock_accounts):
    # INIT #
    util, storage_factory = account_util
    mocked_accounts = mock_accounts()

    storage_factory.enable_auto_sync()
    storage_factory.load_multi_mixed_accounts()

    custom_admin = mocked_accounts.create_account(status=AccountStatus.ADMIN)
    custom_user = mocked_accounts.create_account(status=AccountStatus.USER)
    custom_on_hold = mocked_accounts.create_account(status=AccountStatus.ON_HOLD)
    custom_banned = mocked_accounts.create_account(status=AccountStatus.BANNED)

    storage_factory.save_accounts([custom_admin, custom_user, custom_on_hold, custom_banned])
    storage_factory.build()

    # TEST LOGIC #
    with pytest.raises(PermissionError) as on_hold_forbidden:
        util.read_self(custom_on_hold, 'id', custom_on_hold.id)

    with pytest.raises(PermissionError) as banned_forbidden:
        util.read_self(custom_banned, 'id', custom_banned.id)

    user_not_stored = mocked_accounts.create_account(status=AccountStatus.USER)

    with pytest.raises(ValueError) as user_not_found:
        util.read_self(user_not_stored, 'id', user_not_stored.id)

    user_public_view = util.read_self(custom_user, 'id', custom_user.id)
    admin_public_view = util.read_self(custom_admin, 'id', custom_admin.id)
    confirm_user = storage_factory.query_seeded_data('id', custom_user.id)
    confirm_admin = storage_factory.query_seeded_data('id', custom_admin.id)

    # ASSERTIONS #
    assert f'You cannot complete this operation while your account is {custom_on_hold.status}.' in str(on_hold_forbidden.value)
    assert f'You cannot complete this operation while your account is {custom_banned.status}.' in str(banned_forbidden.value)
    assert 'Account could not be found.' in str(user_not_found.value)

    assert user_public_view.username == custom_user.username
    assert admin_public_view.username == custom_admin.username
    assert custom_user.username == confirm_user.username
    assert custom_admin.username == confirm_admin.username