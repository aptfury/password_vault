'''
AUTHOR: Blake Lemarr
DATE: 05.09.26
DESCRIPTION: Test cases for system storage
'''

import json
import pytest

from pathlib import Path

# -------------- Successes -------------- #

def test_read(tmp_path, app_storage):
    test_db_name: str = 'accounts'
    test_db: Path = tmp_path / f'{test_db_name}.json'
    
    with open(test_db, 'w', encoding='utf-8') as file:
        test_input: dict = {
            'message': 'You read me!'
        }
        json.dump([test_input], file, indent=4)
        
    @app_storage(action='read')
    def read_database(**kwargs):
        pass
    
    res = read_database(test_db_name=test_db_name)

    assert isinstance(res, list)
    assert res[0]['message'] == 'You read me!'

def test_update(tmp_path, app_storage):
    test_db_name: str = 'accounts'
    test_db: Path = tmp_path / f'{test_db_name}.json'
    
    with open(test_db, 'w', encoding='utf-8') as file:
        file.write('[]')
        
    @app_storage(action='write')
    def write_database(**kwargs):
        pass
    
    @app_storage(action='update')
    def update_database(**kwargs):
        pass
    
    @app_storage(action='read')
    def read_database(**kwargs):
        pass
    
    data: dict = {
        'name': 'Lola',
        'sister': 'Candy'
    }
    data_two: dict = {
        'name': 'blake'
    }
    
    data_set: list = [data]
    
    write_database(test_db_name=test_db_name, data=data_set)
    update_database(test_db_name=test_db_name, data=data_two, key='name', value='Lola')
    
    res: list[dict] = read_database(test_db_name=test_db_name)
    
    assert isinstance(res, list)
    assert data_two in res
    
    update_database(test_db_name=test_db_name, data=data)
    
    res = read_database(test_db_name=test_db_name)
    
    assert isinstance(res, list)
    assert data_two in res and data in res

def test_write(tmp_path, app_storage):
    test_db_name: str = 'accounts'
    test_db: Path = tmp_path / f'{test_db_name}.json'
    
    with open(test_db, 'w', encoding='utf-8') as file:
        file.write('[]')
        
    @app_storage(action='write')
    def append_database(**kwargs):
        pass
    
    @app_storage(action='read')
    def read_database(**kwargs):
        pass
    
    
    data: dict = {
        'name': 'Lola',
        'sister': 'Candy'
    }
    data_two: dict = {
        'name': 'blake'
    }
    
    data_set: list = [data, data_two]

    req: None = append_database(test_db_name=test_db_name, data=data_set)
    append_database(test_db_name=test_db_name, data=data_set)
    res: list[dict] = read_database(test_db_name=test_db_name)
    
    assert req is None
    
    assert data in res and data_two in res
    
def test_delete(tmp_path, app_storage):
    test_db_name: str = 'accounts'
    test_db: Path = tmp_path / f'{test_db_name}.json'
    
    with open(test_db, 'w', encoding='utf-8') as file:
        file.write('[]')
        
    @app_storage(action='write')
    def append_database(**kwargs):
        pass
    
    @app_storage(action='read')
    def read_database(**kwargs):
        pass
    
    @app_storage(action='delete')
    def delete_database(**kwargs):
        pass
    
    data: dict = {
        'name': 'Lola',
        'sister': 'Candy'
    }
    data_two: dict = {
        'name': 'blake'
    }
    
    data_set: list = [data, data_two]
    
    append_database(test_db_name=test_db_name, data=data_set)
    append_database(test_db_name=test_db_name, data=data_set)
    
    req: bool = delete_database(test_db_name=test_db_name)
    
    assert isinstance(req, bool)
    assert req

# -------------- Errors -------------- #
def test_action_error(tmp_path, app_storage):
    with pytest.raises(Exception) as e:
        test_db_name: str = 'accounts'
        test_db: Path = tmp_path / f'{test_db_name}.json'
        
        with open(test_db, 'w', encoding='utf-8') as file:
            test_input: dict = {
                'message': 'You read me!'
            }
            json.dump([test_input], file, indent=4)
            
        @app_storage(action='should_not_work')
        def read_database(**kwargs):
            pass
        
        read_database(test_db_name=test_db_name)

        assert e == ConnectionRefusedError or ConnectionAbortedError
        
def test_db_name_error(tmp_path, app_storage):
    with pytest.raises(Exception) as e:
        test_db_name: str = 'not_an_account'
        test_db: Path = tmp_path / f'{test_db_name}.json'
        
        with open(test_db, 'w', encoding='utf-8') as file:
            test_input: dict = {
                'message': 'You read me!'
            }
            json.dump([test_input], file, indent=4)
            
        @app_storage(action='read')
        def read_database(**kwargs):
            pass
        
        read_database(test_db_name=test_db_name)

        assert e == ConnectionRefusedError or ConnectionAbortedError
        
def test_db_dir_error(tmp_path, app_storage):
    with pytest.raises(Exception) as e:
        test_db_name: str = 'accounts'
        test_dir: str = 'not_a_dir'
        test_db: Path = tmp_path / test_dir / f'{test_db_name}.json'
        
        with open(test_db, 'w', encoding='utf-8') as file:
            test_input: dict = {
                'message': 'You read me!'
            }
            json.dump([test_input], file, indent=4)
            
        @app_storage(action='read')
        def read_database(**kwargs):
            pass
        
        read_database(test_dir=test_dir, test_db_name=test_db_name)

        assert e == ConnectionRefusedError or ConnectionAbortedError