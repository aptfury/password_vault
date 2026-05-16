'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Storage decorator for the application.
'''

# ---------- imports ---------- #
# from functools import wraps
# from .storage_config import StorageConfig

class AppStorage():
    def __init__(self, action: str, db_name: str, db_dir: str = 'database'):
        # super().__init__(db_name=db_name, db_dir=db_dir)
        pass
        
#     def __call__(self, func):
#         @wraps(func)
#         def wrapper(**kwargs):
#             try:
#                 if self.action == 'read':
#                     return self.read()
                
#                 if self.action == 'add':
#                     data: dict = kwargs.get('data', None)
#                     return self.add(data)
                
#                 if self.action == 'update':
#                     key: str = kwargs.get('key', None)
#                     value: str = kwargs.get('value', None)
#                     data: dict = kwargs.get('data', None)
                    
#                     return self.update(key, value, data)
                
#                 if self.action == 'delete':
#                     key: str = kwargs.get('key', None)
#                     value: str = kwargs.get('value', None)
                    
#                     return self.delete(key, value)
                
#                 raise ConnectionAbortedError('There was an unknown system error.')

#             except Exception as e:
#                 print(e)
#                 return
