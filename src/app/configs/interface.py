'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: Interface for the repositories.
'''

# ------------ imports ------------ #
from abc import ABC, abstractmethod

# ------------ class ------------ #
class IRepository[T](ABC):
    @abstractmethod
    def create(self, data: T) -> bool:
        ...
        
    @abstractmethod
    def get(self, key: str, value: str) -> T:
        ...
        
    @abstractmethod
    def get_id(self, key: str, value: str) -> str:
        ...
        
    @abstractmethod
    def update(self, key: str, value: str, data: T) -> bool:
        ...
        
    @abstractmethod
    def delete(self, key: str, value: str) -> bool:
        ...