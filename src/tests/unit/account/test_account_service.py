def test_create_new_account(mock_account_service, account_models):
    created = mock_account_service.create(account_models['internal'])

    assert created

