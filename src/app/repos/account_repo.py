'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Repository for fetching account information.

TODO: Run tests
'''

from .config import IRepository
from .config import read_file, update_file

from ..models import AccountModel

class AccountRepo(IRepository[AccountModel]):
    def __init__(self, **kwargs):
        self.db_name = 'accounts' # file name, must exclude file path
        self.is_test = kwargs.get('is_test')
        self.test_dir = kwargs.get('test_dir')
        
    def get_raw_data(self) -> list[dict]:
        """Retrieves the contents of the 'acconts' file.

        Returns:
            list[dict]: The list of dictionaries from the file.
        """        
        if self.is_test:
            return read_file(test_db_name=self.db_name, is_test=self.is_test, test_dir=self.test_dir)
        
        return read_file(db_name=self.db_name)

    def create(self, data: AccountModel) -> bool:
        """Creates a user's account in the database.

        Args:
            data (AccountModel): The model of the user's account information.

        Returns:
            bool: Whether the account has been successfully created
        """        
        # transform data
        user = data.model_dump(by_alias=True, mode='json')
        
        if self.is_test:
            update_file(data=user, test_db_name=self.db_name, is_test=self.is_test, test_dir=self.test_dir)
        else:
            update_file(data=user, db_name=self.db_name)
        
        raw_data: list[dict] = self.get_raw_data()
        
        return user in raw_data
        

    def get_all(self) -> list[AccountModel]:
        """Retrieves all user accounts from the database.

        Returns:
            list[AccountModel]: Returns a list of user accounts as AccountModels
        """        
        raw_data = self.get_raw_data()
        
        return [AccountModel.model_validate(account) for account in raw_data]

    def get_id(self, key: str, value: str) -> str:
        """Returns the account id of the user - for internal use only

        Args:
            key (str): What you are searching to find the account.
                       (i.e. name, email, etc.)
            value (str): The value you are expecting for the account.

        Returns:
            str: The account id.
        """
        raw_data: list[dict] = self.get_raw_data()
        
        for account in raw_data:
            if account[key] == value:
                return account['_id']

    def get_by_id(self, id: str) -> AccountModel:
        """Gets an account by its id

        Args:
            id (str): The id of the account

        Returns:
            AccountModel: The account
        """        
        raw_data: list[dict] = self.get_raw_data()
        
        for account in raw_data:
            if account['_id'] == id:
                return AccountModel.model_validate(account)

    def get_one_where(self, key: str, value: str) -> AccountModel:
        """Retrieves a user account based on specific query

        Args:
            key (str): The account information to look at
            value (str): What the account information should be

        Returns:
            AccountModel: The user's account
        """        
        raw_data: list[dict] = self.get_raw_data()
        
        for account in raw_data:
            if account[key] == value:
                return AccountModel.model_validate(account)

    def get_all_where(self, key: str, value: str, limit: int | bool = False) -> list[AccountModel]:
        """Retrieves multiple acounts matching the search criteria

        Args:
            key (str): The account information to find
            value (str): The information it should match
            limit (int | bool, optional): A limit on accounts returned. Defaults to False.

        Returns:
            list[AccountModel]: The list of accounts matching the search criteria.
        """        
        raw_data: list[dict] = self.get_raw_data()
        accounts: list[AccountModel] = []
        
        for account in raw_data:
            if account[key] == value:
                accounts.append(AccountModel.model_validate(account))
                
                if limit and len(accounts) >= limit:
                    break
        
        return accounts
                    
    def update_one_where(self, data: AccountModel, key: str, value: str) -> bool:
        """Updates a user's account information based on the search criteria

        Args:
            data (AccountModel): The data to be inserted.
            key (str): The account information to find
            value (str): The information it should match

        Returns:
            bool: Update successful
        """
        user_id: str = self.get_id(key, value)
        
        if user_id is None:
            raise ValueError('No updates could be performed as the ID could not be found.')
        
        original_user: AccountModel = self.get_by_id(user_id)
        
        if original_user == data:
            raise ValueError('No updates have been made.')
        
        data.id = original_user.id
        data.created = original_user.created
        data_dump = data.model_dump(by_alias=True, mode='json')

        if self.is_test:
            update_file(test_db_name=self.db_name, data=data_dump, key=key, value=value, is_test=self.is_test, test_dir=self.test_dir)
        else:
            update_file(db_name=self.db_name, data=data_dump, key=key, value=value)
        
        raw_data: list[dict] = self.get_raw_data()
        
        return data_dump in raw_data

    def delete_one_where(self, key: str, value: str) -> bool:
        """Deletes a user account from the database - ** will be updated to remove related files **
        TODO: Ensure cascading deletion when user is removed.
        TODO: Move to temp_deletion.json for safety for up to 5 days before permanently deleting.

        Args:
            key (str): The account information to find
            value (str): The information it should match

        Returns:
            bool: Delete successful
        """        
        user: AccountModel = self.get_one_where(key=key, value=value)
        
        if user is None:
            raise LookupError('The user could not be found.')
        
        user_dump = user.model_dump(by_alias=True, mode='json')
        
        if self.is_test:
            update_file(test_db_name=self.db_name, data=None, key=key, value=value, is_test=self.is_test, test_dir=self.test_dir)
        else:
            update_file(db_name=self.db_name, data=None, key=key, value=value)
            
        raw_data: list[dict] = self.get_raw_data()
        
        return not user_dump in raw_data
        

    def delete_all_where(self, key: str, value: str) -> bool:
        pass

    def delete_database(self) -> bool:
        pass