'''
AUTHOR: Blake Lemarr
DATE: 05.13.26
DESCRIPTION: Test case for account service
'''

# ------------ IMPORTS ------------ #
import json
import pytest

from app.models import AccountModel

# ------------ ACOUNT SERVICE TESTS ------------ #
def test_account_service(monkeypatch, tmp_path, account_service, account_repo, capsys):
    ################### SERVICE INIT ###################
    inputs = iter(['ThisName', 'ThisPassword', 'ThisPassword', 'this@email.com', 'ThisName', 'ThisPassword', '1', 'ThisName', 'TestName', '2', 'this@email.com', 'email@test.com', 'y', 'TestName', 'ThisPassword', '3', '1', 'TestName', 'ThisName'])
    
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
      
    test_dir = tmp_path / 'database'
    test_dir.mkdir(parents=True, exist_ok=True)
    
    test_path = test_dir / 'accounts.json'
    
    with open(test_path, 'w', encoding='utf-8') as file:
        json.dump([], file, indent=4)
    ###################################################

    ################### NEW ACCOUNT ###################
    account_service.create_account()
    
    repo = account_repo(is_test=True, test_dir=test_dir)
    
    user: AccountModel = repo.get_one_where('name', 'ThisName')
    
    assert user.name == 'ThisName'
    assert user.email == 'this@email.com'
    ###################################################

    ################### LOGGING IN ###################
    logged_in: bool = account_service.login()
    
    assert logged_in
    assert account_service.auth.access_granted()
    assert len(account_service.name) == 8
    assert account_service._id == user.id
    assert account_service.session_id == account_service.encrypt._fernet
    ###################################################
    
    ################### VIEW ACCOUNT ###################
    account_service.view_account()
    
    # captured = capsys.readouterr()
    
    # assert 'USER ACCOUNT DETAILS' in captured.out
    # assert 'ThisName' in captured.out
    # assert 'this@email.com' in captured.out
    
    # print(captured)
    # capsys.close()
    ###################################################
    
    ################# UPDATE ACCOUNT #################
    account_service.update_account()
    account_service.update_account()
    
    # updated to TestName and email@test.com
    user: AccountModel = repo.get_one_where('name', 'TestName')
    
    assert user.name == 'TestName'
    assert user.email == 'email@test.com'
    assert account_service.name == 'TestName'
    assert account_service._id == user.id
    assert account_service.session_id == account_service.encrypt._fernet
    ###################################################
    
    ################### LOGGING OUT ###################
    with pytest.raises(SystemExit) as good_exit:
        account_service.logout()
        assert good_exit
    ###################################################
    
    ################## ACCOUNT MENU ##################
    account_service.login()
    account_service.account_menu()
    account_service.account_menu()
    #################################################