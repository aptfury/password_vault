'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Unit tests for the database
'''

# ------------ imports ------------ #
import json
from pathlib import Path
from src.app.configs.database import Database

# ------------ class ------------ #
class TestDatabase:
    def test_initialized(self, account_database):
        db: Database = account_database
        assert db.initialized()
        
    def test_read(self, account_database):
        db: Database = account_database
        assert db.initialized()
        
        data: dict = {
            'name': 'lola'
        }
        
        # create something to read
        with open(db.db_path, 'w', encoding='utf-8') as file:
            json.dump([data], file, indent=4)
            
        returned_data: list[dict] = db.read()
        
        assert data in returned_data
        
    def test_add(self, account_database):
        db: Database = account_database
        assert db.initialized()
        
        data: dict = {
            'name': 'lola'
        }
        
        success: bool = db.add(data)
        
        returned_data: list[dict] = db.read()
        
        assert success
        assert data in returned_data
        
    def test_update(self, account_database):
        db: Database = account_database
        assert db.initialized()
        
        lola: dict = {
            'name': 'lola'
        }
        
        success: bool = db.add(lola)
        assert success
        
        candy: dict = {
            'name': 'candy'
        }
        
        success: bool = db.add(candy)
        assert success

        data: dict = {
            'name': 'lola',
            'father': 'blake',
            'mother': 'alexx'
        }
        
        success: bool = db.update('name', 'lola', data)
        returned_data: list[dict] = db.read()
        
        assert success
        assert lola not in returned_data
        assert candy in returned_data
        assert data in returned_data
        
    def test_delete(self, account_database):
        db: Database = account_database
        assert db.initialized()
        
        lola: dict = {
            'name': 'lola'
        }
        candy: dict = {
            'name': 'candy'
        }
        
        db.add(lola)
        db.add(candy)
        
        success: bool = db.delete('name', 'candy')
        returned_data: list[dict] = db.read()
        
        assert success
        assert lola in returned_data
        assert candy not in returned_data
        
    def test_mock(self, mock_database):
        data: list[dict] = [
            {
                'name': 'lola',
                'father': 'blake',
                'mother': 'alexx'
            },
            {
                'name': 'candy',
                'father': 'gordon',
                'mother': 'daniella'
            }
        ]
        
        db: Database = mock_database('accounts.json', data)
        
        assert db.initialized()
        assert data == db.read()
        assert db.add(data) and db.update('name', 'lola', data[0]) and db.delete('name', 'lola')