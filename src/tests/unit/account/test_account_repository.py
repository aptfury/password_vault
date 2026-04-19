from app.models import AccountStatus


def test_working_create(account_repo, mock_accounts):
    # INIT #
    repo, storage_factory = account_repo
    storage_factory.enable_auto_sync()
    mocked_storage = storage_factory.build()
    mocked_accounts = mock_accounts()

    # TEST LOGIC #
    test_user = mocked_accounts.create_account()
    created = repo.create(test_user, 'TEST_ADMIN')
    data = mocked_storage.load_data()

    expected_data = [test_user.model_dump(mode='json')]

    # ASSERTIONS #
    assert created
    assert len(data) == 1
    assert data == expected_data

def test_working_get_all(account_repo):
    # INIT #
    repo, storage_factory = account_repo
    storage_factory.enable_auto_sync()
    storage_factory.load_multi_mixed_accounts(total_accounts=10)
    mocked_storage = storage_factory.build()

    # TEST LOGIC #
    result = repo.get_all()
    data = mocked_storage.load_data()

    expected_length = len(result)
    expected_data = result

    # ASSERTIONS #
    assert len(data) == expected_length
    assert data == expected_data

def test_working_read(account_repo, mock_accounts):
    # INIT #
    repo, storage_factory = account_repo
    mocked_accounts = mock_accounts()
    storage_factory.enable_auto_sync()
    storage_factory.load_multi_mixed_accounts(total_accounts=10)

    custom_admin = mocked_accounts.create_account(status=AccountStatus.ADMIN)
    custom_user = mocked_accounts.create_account(status=AccountStatus.USER)

    storage_factory.save_accounts([custom_admin, custom_user])
    storage_factory.build()

    # TEST LOGIC #
    read_by_status_result = repo.read('status', AccountStatus.ADMIN, custom_admin.id)
    read_by_status_actual = storage_factory.query_seeded_data('status', AccountStatus.ADMIN)

    expected_read_by_status_length = len(read_by_status_actual)
    expected_read_by_status_data = read_by_status_actual

    read_by_id_result = repo.read('id', custom_user.id, custom_admin.id)
    read_by_id_actual = storage_factory.query_seeded_data('id', custom_user.id)

    expected_read_by_id_length = len(read_by_id_actual)
    expected_read_by_id_data = read_by_id_actual

    read_by_pii_email_result = repo.read('pii_email', custom_user.pii_email, custom_admin.id)
    read_by_email_result = repo.read('email', custom_user.pii_email, custom_admin.id)
    read_by_pii_email_actual = storage_factory.query_seeded_data('pii_email', custom_user.pii_email)

    expected_read_by_pii_email_length = len(read_by_pii_email_actual)
    expected_read_by_pii_email_data = read_by_pii_email_actual

    read_by_username_result = repo.read('username', custom_user.username, custom_admin.id)
    read_by_username_actual = storage_factory.query_seeded_data('username', custom_user.username)

    expected_read_by_username_length = len(read_by_username_actual)
    expected_read_by_username_data = read_by_username_actual

    # ASSERTIONS #
    assert len(read_by_status_result) == expected_read_by_status_length
    assert read_by_status_result == expected_read_by_status_data
    assert any(a.id == custom_admin.id for a in read_by_status_result)

    assert len(read_by_id_result) == expected_read_by_id_length
    assert read_by_id_result == expected_read_by_id_data

    assert len(read_by_pii_email_result) == expected_read_by_pii_email_length
    assert read_by_pii_email_result == expected_read_by_pii_email_data
    assert len(read_by_email_result) == expected_read_by_pii_email_length
    assert read_by_email_result == expected_read_by_pii_email_data

    assert len(read_by_username_result) == expected_read_by_username_length
    assert read_by_username_result == expected_read_by_username_data

def test_working_update(account_repo, mock_accounts):
    # INIT #
    repo, storage_factory = account_repo
    mocked_accounts = mock_accounts()
    storage_factory.enable_auto_sync()
    storage_factory.load_multi_mixed_accounts(total_accounts=10)

    custom_admin = mocked_accounts.create_account(status=AccountStatus.ADMIN)
    custom_user = mocked_accounts.create_account()

    storage_factory.save_accounts([custom_admin, custom_user])
    storage_factory.build()

    # TEST LOGIC #
    updated_custom_user = mocked_accounts.create_account()
    updated_custom_user.id = custom_user.id

    updated = repo.update(custom_user.id, updated_custom_user, custom_admin.id)
    find_user = storage_factory.query_seeded_data('id', custom_user.id)

    expected_result = [updated_custom_user]

    # ASSERTIONS #
    assert custom_user.id == updated_custom_user.id
    assert updated
    assert find_user == expected_result

def test_working_delete(account_repo, mock_accounts):
    # INIT #
    repo, storage_factory = account_repo
    mocked_accounts = mock_accounts()
    storage_factory.enable_auto_sync()
    storage_factory.load_multi_mixed_accounts(total_accounts=10)

    custom_admin = mocked_accounts.create_account(status=AccountStatus.ADMIN)
    custom_user = mocked_accounts.create_account()

    storage_factory.save_accounts([custom_admin, custom_user])
    storage_factory.build()

    # TEST LOGIC #
    deleted = repo.delete(custom_user.id, 'running tests', custom_admin.id)
    try_find_user = storage_factory.query_seeded_data('id', custom_user.id)
    all_accounts = storage_factory.load_data()

    expected_try_find_user = []

    # ASSERTIONS #
    assert deleted
    assert try_find_user == expected_try_find_user
    assert not any(acc.id == custom_user.id for acc in all_accounts)