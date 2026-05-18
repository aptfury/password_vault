'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: A repository to manage account transactions
'''

# ------------ imports ------------ #
from ..configs import (
    AccountModel,
    Database,
    IRepository
)

# ------------ class ------------ #
class AccountRepo(IRepository[AccountModel]):
    def __init__(self, database: Database):
        self.db: Database = database
        self.is_connected = self.db.initialized()
        
    def create(self, data: AccountModel) -> bool:
        """Creates an account in the accounts database.

        Args:
            data (AccountModel): The data model of the user account

        Returns:
            bool: If it was created successfully
        """        
        data_dump: dict = data.model_dump(by_alias=True, mode='json')
        return self.db.add(data_dump)

    def get(self, key: str, value: str) -> AccountModel:
        """Retrieves the queried account from the accounts database

        Args:
            key (str): The specific user data to query
            value (str): What the user data should be

        Returns:
            AccountModel: The populated data model for that account
        """        
        accounts: list[dict] = self.db.read()
        target: dict = None
        for account in accounts:
            if account[key] == value:
                target = account
                break
        
        return AccountModel.model_validate(target)

    def get_id(self, key: str, value: str) -> str:
        """Retreives the ID of the specified account

        Args:
            key (str): The specific user data to query
            value (str): What the user data should be

        Returns:
            str: The account's ID
        """        
        accounts: list[dict] = self.db.read()
        target: dict = None

        for account in accounts:
            if account[key] == value:
                target = account

        return target['_id']

    def update(self, key: str, value: str, data: AccountModel) -> bool:
        """Updates the given account with the new data

        Args:
            key (str): The specific user data to query
            value (str): What the user data should be
            data (AccountModel): The data model of the updated information

        Returns:
            bool: If the update was successful
        """        
        data_dump: dict = data.model_dump(by_alias=True, mode='json')
        return self.db.update(key, value, data_dump)
    
    def delete(self, key: str, value: str) -> bool:
        """Deletes an account based on the provided information

        Args:
            key (str): The specific user data to query
            value (str): What the user data should be

        Returns:
            bool: If the deletion was successful
        """        
        return self.db.delete(key, value)