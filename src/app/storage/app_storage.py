'''
AUTHOR: Blake Lemarr
DATE: 05.10.26
DESCRIPTION: A subclass of StorageConfig made to function as a wrapper for
                repository access.
'''

from pathlib import Path
from typing import Optional
from functools import wraps

from .storage_config import StorageConfig

class AppStorage(StorageConfig):
    def __init__(self, action: str, **kwargs):
        self.valid_action: bool = self.__validate_data(key='action', value=action)
        self.action: Optional[str] = action if self.valid_action else None
        
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            db_name: str = func()
            if not self.__validate_data(key='db_name', value=db_name):
                raise ConnectionRefusedError(f'There is not database by the name of {db_name}')
            
            self.__db_name = db_name
            self.__build_path()
            
            return self.__parse_operation(**kwargs)
        return wrapper
        
    def __parse_operation(self, **kwargs) -> Optional[list[dict]]:
        actions: dict = {
            'test': self.__build_path(),
            'read': self.__read(),
            'append': self.__append(kwargs.get('data')),
            'write': self.__write(kwargs.get('data')),
            'delete': self.__delete()
        }
        
        if self.action is None:
            raise ConnectionAbortedError('The requested action is not available.')
        
        return actions[self.action]