'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Test suite for system controller
'''

# ------------ imports ------------ #
import pytest
from src.app.controllers.system_controller import SystemController

# ------------ class ------------ #
class TestSystemController:
    def test_create_account(self, system_controller, monkeypatch, capsys):
        inputs = iter(['blake', 'lola', 'blake.lola@gmail.com', '3'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        with pytest.raises(SystemExit) as exec_info:
            system_controller.create_account()
            
            captured = capsys.readouterr()
            
            assert 'Account created! Please log in to continue.' in captured.out
            
            assert exec_info
            
    def test_login(self, system_controller, monkeypatch, capsys):
        inputs = iter(['2','blake', 'lola', 'blake.lola@gmail.com', '1', 'blake', 'lola', '4'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        system_controller.main_menu()
        
        captured = capsys.readouterr()
        
        assert 'ACCOUNT MENU' in captured.out
        assert 'blake' in captured.out
        
    def test_cycle_account(self, system_controller, monkeypatch, capsys):
        inputs = iter(['blake', 'lola', 'blake@gmail.com', '1', 'blake', 'lola', '1', '4', '4', '1', '5', '4'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        system_controller.create_account()
        
        # system_controller.log_in()
        
        system_controller.cycle_account()
        
        captured = capsys.readouterr()
        
        assert 'ACCOUNT MENU' in captured.out
        assert 'VAULT MENU' in captured.out
        assert 'PASSWORD' in captured.out
        assert 'ACCOUNT MENU' in captured.out
        assert 'VAULT MENU' in captured.out