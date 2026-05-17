'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: A repository to manage vault transactions
'''

# ------------ imports ------------ #
from pathlib import Path
from ..configs import (
    VaultModel,
    Database,
    IRepository
)

# ------------ class ------------ #
app_dir: Path = Path(__file__).resolve().parent.parent
db_dir: Path = app_dir / 'database'
db_file: Path = db_dir / 'vaults.json'
class VaultRepo(IRepository[VaultModel]):
    def __init__(self):
        self.db: Database = Database(db_path=db_file)
        self.is_connected = self.db.initialized()
        
    def create(self, data: VaultModel) -> bool:
        """Creates an vault in the vaults database.

        Args:
            data (VaultModel): The data model of the user vault

        Returns:
            bool: If it was created successfully
        """        
        data_dump: dict = data.model_dump(by_alias=True, mode='json')
        return self.db.add(data_dump)

    def get(self, key: str, value: str) -> VaultModel:
        """Retrieves the queried vault from the vaults database

        Args:
            key (str): The specific user data to query
            value (str): What the user data should be

        Returns:
            VaultModel: The populated data model for that vault
        """        
        vaults: list[dict] = self.db.read()
        target: dict = None
        for vault in vaults:
            if vault[key] == value:
                target = vault
                break
        
        return VaultModel.model_validate(target)

    def get_id(self, key: str, value: str) -> str:
        """Retreives the ID of the specified vault

        Args:
            key (str): The specific user data to query
            value (str): What the user data should be

        Returns:
            str: The vault's ID
        """        
        vaults: list[dict] = self.db.read()
        target: dict = None

        for vault in vaults:
            if vault[key] == value:
                target = vault

        return target['_id']

    def update(self, key: str, value: str, data: VaultModel) -> bool:
        """Updates the given vault with the new data

        Args:
            key (str): The specific user data to query
            value (str): What the user data should be
            data (VaultModel): The data model of the updated information

        Returns:
            bool: If the update was successful
        """        
        data_dump: dict = data.model_dump(by_alias=True, mode='json')
        return self.db.update(key, value, data_dump)
    
    def delete(self, key: str, value: str) -> bool:
        """Deletes an vault based on the provided information

        Args:
            key (str): The specific user data to query
            value (str): What the user data should be

        Returns:
            bool: If the deletion was successful
        """        
        return self.db.delete(key, value)