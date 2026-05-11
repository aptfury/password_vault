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
        super().__init__(**kwargs)
        
        self.valid_action: bool = self.validate_data(key='action', value=action)
        self.action: Optional[str] = action if self.valid_action else None
        
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            db_name: str = kwargs.get('db_name') or kwargs.get('test_db_name')
            
            if not self.is_test:
                self.db_name = db_name
            else:
                self.test_db_name = db_name
                
            self.build_path()
            
            return self.__parse_operation(**kwargs)
        return wrapper
        
    def __parse_operation(self, **kwargs) -> Optional[list[dict]]:
        if not self.valid_action or self.action is None:
            # TODO: Replace error
            raise ConnectionAbortedError('The requested action is not available.')
       
        if self.action == 'read':
            return self.read(**kwargs)
        
        if self.action == 'update':
            return self.update(**kwargs)
        
        if self.action == 'write':
            return self.write(**kwargs)
        
        if self.action == 'delete':
            return self.delete(**kwargs)