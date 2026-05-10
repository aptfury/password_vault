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
        
    def __init_subclass__(cls, **kwargs):
        
        super().__init_subclass__(cls, **kwargs)
        
        def _database_exists() -> bool:
            return cls.__build_path(cls).exists()
        
        def read() -> list[dict]:
            return cls.__read(cls)
        
        def append(data: dict) -> None:
            return cls.__append(cls, data)
        
        def write(data: dict) -> None:
            return cls.__write(cls, data)
        
        def delete() -> None:
            return cls.__delete(cls)
        

    def __init__(self, **kwargs):
        ### NOTE: FOR TESTING ONLY ###
        self.is_test: bool = kwargs.get('is_test', False)
        self.test_dir: Optional[Path] = kwargs.get('test_dir', None)
        self.test_db_name: Optional[str] = kwargs.get('test_db_name', None)

        ### Fill in available ###
        self.__db_name: Optional[str] = kwargs.get('db_name', None)
        self.__db_dir: Optional[str] = kwargs.get('db_dir', None)


    ### VALIDATE DATABASE NAME ###
    def __validate_data(self, **kwargs) -> bool:
        '''Checks the submitted data against valid data sets'''

        # validation sets
        valid_data_set: dict = {
            'actions': ['test', 'read', 'append', 'write', 'delete'],
            'db_name': ['tests', 'accounts', 'vaults', 'logs', 'security'],
            'db_dir': ['tests', 'tmp_dir', 'database', 'logs']
        }

        # key and value pairs as kwargs
        # add more to be added as needed
        key: str = kwargs.get('key', None)
        value: Any = kwargs.get('value', None)

        # return boolean
        return value in valid_data_set[key]


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

    ### READ ###
    def __read(self) -> list[dict]:
        db: Path = self.__build_path()
        data: list[dict] = []
        
        with open(db, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # TODO: Turn into a log later
        print('data accessed')
        return data
    
    ### APPEND ###
    def __append(self, data: dict) -> None:
        db: Path = self.__build_path()
        
        with open(db, 'a', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            
        # TODO: Turn into a log later
        print('data appended')
        return
    
    ### WRITE ###
    def __write(self, data: dict | list[dict]) -> None:
        db: Path = self.__build_path()
        
        with open(db, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            
        # TODO: Turn into a log later
        # REFACTOR: Can probably be combined with __appened()
        # with an arg to call 'a' or 'w' dynamically.
        print('data overwritten')
        return
    
    ### DELETE ###
    # Do not use this to delete content, it should
    # only be used to delete the actual databse file.
    # If you want to erase all the file contents, use
    # __write() instead.
    def __delete(self) -> None:
        db: Path = self.__build_path()
        db.unlink(missing_ok=True)
        
        # TODO: Turn into a log later
        print('database deleted')
        return
    
    