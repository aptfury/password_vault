'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Repository for fetching account information.
'''

from .config import IRepository
from .config import read_file, update_file, delete_file

from ..models import AccountModel

class AccountRepo(IRepository[AccountModel]):
    def __init__(self):
        self.db_name = 'accounts'
        
    def get_raw_data(self) -> list[dict]:
        return read_file(db_name=self.db_name)

    def create(self, data: AccountModel) -> bool:
        
        update_file(db_name=self.db_name, data=data)
        
        raw_data: list[dict] = self.get_raw_data()
        
        return data in raw_data

    def get_all(self) -> list[AccountModel]:
        raw_data: list[dict] = self.get_raw_data()
        
        return [AccountModel.model_validate(account) for account in raw_data]

    def get_id(self, key: str, value: str) -> str:
        raw_data: list[dict] = self.get_raw_data()
        
        for account in raw_data:
            if account[key] == value:
                return account['_id']

    def get_by_id(self, id: str) -> AccountModel:
        raw_data: list[dict] = self.get_raw_data()
        
        for account in raw_data:
            if account['_id'] == id:
                return AccountModel.model_validate(account)

    def get_one_where(self, key: str, value: str) -> AccountModel:
        raw_data: list[dict] = self.get_raw_data()
        
        for account in raw_data:
            if account[key] == value:
                return AccountModel.model_validate(account)

    def get_all_where(self, key: str, value: str, limit: int | bool = False) -> list[AccountModel]:
        raw_data: list[dict] = self.get_raw_data()
        
        accounts: list[AccountModel] = []
        
        for account in raw_data:
            if account[key] == value:
                accounts.append(AccountModel.model_validate(account))
                if limit and len(accounts) >= limit:
                    break
                        
        return accounts   
                    
    def update_one_where(self, data: AccountModel, key: str, value: str) -> bool:
        update_file(db_name=self.db_name, data=data, key=key, value=value)
        
        raw_data: list[dict] = self.get_raw_data()
        for account in raw_data:
            if account[key] == value:
                return AccountModel.model_validate(account) == data

    def delete_one_where(self, key: str, value: str) -> bool:
        update_file(db_name=self.db_name, data=None, key=key, value=value)
        
        raw_data: list[dict] = self.get_raw_data()
        deleted: bool = True

        for account in raw_data:
            if account[key] == value:
                deleted = False

        return deleted

    def delete_all_where(self, key: str, value: str) -> bool:
        for _ in self.get_raw_data():
            update_file(db_name=self.db_name, data=None, key=key, value=value)
            
        deleted: bool = True

        raw_data: list[dict] = self.get_raw_data()
        
        for account in raw_data:
            if account[key] == value:
                deleted = False

        return deleted

    def delete_database(self) -> bool:
        return delete_file(db_name=self.db_name)