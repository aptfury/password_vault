'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: 
'''

# ------------ imports ------------ #
import pytest
from src.app.main import main

# ------------ class ------------ #
class TestApplication:
    def test_exit_option(self, monkeypatch):
        inputs = iter(['3'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        with pytest.raises(SystemExit) as exec_info:
            main()
            assert exec_info
            
    def test_invalid_option(self, monkeypatch):
        inputs = iter(['invalid_option'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        with pytest.raises(ValueError) as exec_info:
            main()
            assert exec_info