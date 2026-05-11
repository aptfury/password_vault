'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: An interface for the repositories.
'''

from abc import ABC, abstractmethod

class IRepository[T](ABC):
    @abstractmethod
    def connect(self, dir: str, file: str) -> None:
        ...
    
    @abstractmethod
    def create(self, data: T) -> bool:
        ...
        
    @abstractmethod
    def get_all(self) -> list[T]:
        ...
        
    @abstractmethod
    def get_id(self, key: str, value: str) -> str:
        ...
        
    @abstractmethod
    def get_by_id(self, id: str) -> T:
        ...
        
    @abstractmethod
    def get_one_where(self, key: str, value: str) -> T:
        ...
        
    @abstractmethod
    def get_all_where(self, key: str, value: str, limit: int | bool = False) -> list[T]:
        ...
        
    @abstractmethod
    def update_one_where(self, key: str, value: str) -> bool:
        ...
        
    @abstractmethod
    def update_all_where(self, key: str, value: str) -> bool:
        ...
        
    @abstractmethod
    def delete_one_where(self, key: str, value: str) -> bool:
        ...
        
    @abstractmethod
    def delete_all_where(self, key: str, value: str) -> bool:
        ...
        
    @abstractmethod
    def delete_database(self) -> bool:
        ...