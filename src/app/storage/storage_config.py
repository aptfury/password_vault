'''
AUTHOR: Blake Lemarr
DATE: 05.09.26
DESCRIPTION: A base class for a storage-based decorator.
'''

import json

from pathlib import Path
from typing import Optional, Any

# only use through appropriate subclasses
class StorageConfig:
    def __init__(self, **kwargs):
        ### NOTE: FOR TESTING ONLY ###
        self.is_test: bool = kwargs.get('is_test', False)
        self.test_dir: Optional[Path] = kwargs.get('test_dir', None)
        self.test_db_name: Optional[str] = kwargs.get('test_db_name', None)

        ### Fill in available ###
        self.__db_name: Optional[str] = kwargs.get('db_name', None)
        self.__db_dir: Optional[str] = kwargs.get('db_dir', None)

    @property
    def db_name(self) -> Optional[str]:
        return self.__db_name
    
    @property
    def db_dir(self) -> Optional[str]:
        return self.__db_dir

    ### VALIDATE DATABASE NAME ###
    def __validate_data(self, **kwargs) -> bool:
        '''Checks the submitted data against valid data sets'''

        # validation sets
        valid_data_set: dict = {
            'action': ['test', 'read', 'update', 'write', 'delete'],
            'db_name': ['test', 'accounts', 'vaults', 'logs', 'security'],
            'db_dir': ['test', 'tmp_dir', 'database', 'logs']
        }

        # key and value pairs as kwargs
        # add more to be added as needed
        key: str = kwargs.get('key', None)
        value: Any = kwargs.get('value', None)

        # return boolean
        return value in valid_data_set[key]

    @property
    def validate_data(self) -> function:
        return self.__validate_data

    ### BUILD FILE PATH ###
    def __build_path(self) -> Path:
        '''Builds a path to the database files.'''

        # returns tests path if tests
        if self.is_test:
            if not self.__validate_data(key='db_name', value=self.test_db_name):
                raise ConnectionRefusedError(f'{self.test_db_name} is not a valid database.')
            
            return self.test_dir / f'{self.test_db_name}.json'

        # starts path creation
        src_dir: Path = Path(__file__).resolve().parent
        db_dir: Path = src_dir

        # uses default dir if one was not provided
        # checks provided dir against allowable dirs
        #### TODO: change ConnectionRefusedError()
        # sets moves path to dir if dir is valid
        if self.__db_dir is None:
            db_dir = db_dir.joinpath('database')
        else:
            if not self.__validate_data(key='db_dir', value=f'{self.__db_dir}'):
                raise ConnectionRefusedError(f'{self.__db_dir} is not a valid directory.')

            db_dir: Path = db_dir.joinpath(self.__db_dir)

        # create dir if dir is valid but does not exist
        if not db_dir.exists() or not db_dir.is_dir():
            db_dir.mkdir(parents=True, exist_ok=True)

        # checks if db name is None
        # validates db name against allowed databases
        #### TODO: change ConnectionRefusedError()
        if self.__db_name is None:
            raise ConnectionRefusedError('No database name has been provided.')
        else:
            if not self.__validate_data(key='db_name', value=self.__db_name):
                raise ConnectionRefusedError(f'{self.__db_name} is not a valid database.')

        # move path to database file
        db: Path = db_dir / f'{self.__db_name}.json'

        # create database file if valid and none
        if not db.exists() or not db.is_file():
            db.touch(exist_ok=True)

        # only return db if path to db intact
        if db_dir.exists() and db.exists():
            return db
        # create issue summary
        # raise error if no checks passed
        #### TODO: change FileNotFoundError()
        else:
            issue_summary: dict = {
                'path': str(db),
                'attempted_rebuild_dir': True,
                'attempted_rebuild_db': True,
            }
            
            print(issue_summary)
            raise FileNotFoundError('Failed despite rebuild attempts.')

    @property
    def build_path(self) -> function:
        return self.__build_path

    ### READ ###
    def __read(self, **kwargs) -> list[dict]:
        db: Path = self.__build_path()
        
        with open(db, 'r', encoding='utf-8') as file:
            # TODO: Turn into a log later
            print('data accessed')
            return json.load(file)
            
    @property
    def read(self) -> function:
        return self.__read
    
    ### UPDATE ###
    def __update(self, data: dict, **kwargs) -> None:
        key: str = kwargs.get('key') or None
        value: str = kwargs.get('value') or None
        
        file: list[dict] = self.__read()
        
        if key is not None and value is not None:
            target: dict = {}
            
            for entry in file:
                if entry[key] == value:
                    target = entry

            file.remove(target)
            
        file.append(data)
        
        self.__write(data=file)
        
        print('data updated')
        return
    
    @property
    def update(self) -> None:
        return self.__update
    
    ### WRITE ###
    def __write(self, data: dict | list[dict], **kwargs) -> None:
        db: Path = self.__build_path()
        
        with open(db, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            
        # TODO: Turn into a log later
        # REFACTOR: Can probably be combined with __appened()
        # with an arg to call 'a' or 'w' dynamically.
        print('data overwritten')
        return
    
    @property
    def write(self) -> function:
        return self.__write
    
    ### DELETE ###
    # Do not use this to delete content, it should
    # only be used to delete the actual databse file.
    # If you want to erase all the file contents, use
    # __write() instead.
    def __delete(self, **kwargs) -> bool:
        db: Path = self.__build_path()
        db.unlink(missing_ok=True)
        
        # TODO: Turn into a log later
        print('database deleted')
        return not db.exists()
    
    @property
    def delete(self) -> function:
        return self.__delete