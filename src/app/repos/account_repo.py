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
        # FIX: Currently not worrking
        # transform data
        user = data.model_dump(mode='json')
        
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
        pass

    def get_id(self, key: str, value: str) -> str:
        pass

    def get_by_id(self, id: str) -> AccountModel:
        pass

    def get_one_where(self, key: str, value: str) -> AccountModel:
        pass

    def get_all_where(self, key: str, value: str, limit: int | bool = False) -> list[AccountModel]:
        pass
                    
    def update_one_where(self, data: AccountModel, key: str, value: str) -> bool:
        pass

    def delete_one_where(self, key: str, value: str) -> bool:
        pass

    def delete_all_where(self, key: str, value: str) -> bool:
        pass

    def delete_database(self) -> bool:
        pass