'''
AUTHOR: Blake Lemarr
DATE: 05.09.26

'''

import json

from pathlib import Path
from typing import Any

# only use through appropriate subclasses
class StorageConfig:
    # initiate subclass
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def __init__(self, **kwargs):
        ### Check if running a tests ###
        self.is_test: bool = kwargs.get('is_test', False)
        self.test_dir: Path = kwargs.get('test_dir', None)
        self.test_db_name: str = kwargs.get('test_db_name', None)
        ### Check if running a tests ###

        ### Fill in available ###
        self.__db_name: str = kwargs.get('db_name', None)
        self.__db_dir: str = kwargs.get('db_dir', None)
        ### Fill in available ###

        ### Path builder shortcut ###
        self._database: Path = self.__connect()

    ### VALIDATE DATABASE NAME ###
    def __validate_data(self, **kwargs) -> bool:
        '''Checks the submitted data against valid data sets'''

        # validation sets
        valid_data_set: dict = {
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
    def __connect(self) -> Path:
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