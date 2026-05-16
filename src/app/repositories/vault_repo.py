'''
AUTHOR: Blake Lemarr
DATE: 05.14.26
DESCRIPTION: A repository for managing vault operations
'''

# ------------ IMPORTS ------------ #
from pathlib import Path

from .config import IRepository
from .config import read_vaults, add_vault, update_vault, delete_vault

from ..models import VaultModel

from ..utilities import EncryptUtils

# ------------ VAULT REPO ------------ #
class VaultRepo(IRepository[VaultModel]):
    def __init__(self, **kwargs):
        # test config
        self.is_test: bool = kwargs.get('is_test') or False
        self.test_dir: Path = kwargs.get('test_dir') or None
        
        # database config
        self.db_name: str = 'vaults'
        self.vault_id: str = kwargs.get('vault_id') or None
        self.session: EncryptUtils = kwargs.get('session') or None

    # def __get_raw_vaults(self) -> list | None:
    #     if self.is_test:
    #         return read_file(test_db_name=self.db_name, is_test=self.is_test, test_dir=self.test_dir)
        
    #     return read_file(db_name=self.db_name)
    
    # def __get_raw_vault(self) -> list | None:
    #     raw_vaults = self.__get_raw_vaults()
        
    #     for vault in raw_vaults:
    #         if vault['_id'] == self.vault_id:
    #             return vault
            
    # def __encrypt_login(self, login: dict) -> str | bytes:
    #     return self.session.encrypt(login)
    
    # def __decrypt_login(self, login: str | bytes) -> dict:
    #     return self.session.decrypt_vault(login)
    
    # def create(self, data: VaultModel) -> bool:
    #     raw_data = self.__get_raw_vaults()
    #     vault = data.model_dump(by_alias=True, mode='json')
    #     raw_data.append(vault)
        
    #     if self.is_test:
    #         update_file(data=vault, test_db_name=self.db_name, is_test=self.is_test, test_dir=self.test_dir)
    #     else:
    #         update_file(data=vault, db_name=self.db_name)
            
    #     raw_data = self.__get_raw_vaults()
    #     return vault in raw_data
    
    # def get_all(self) -> list[VaultModel]:
    #     raw_data = self.__get_raw_vaults()
        
    #     return [VaultModel.model_validate(vault) for vault in raw_data]

    # def get_id(self, key: str, value: str) -> str:
    #     raw_data = self.__get_raw_vaults()
        
    #     for vault in raw_data:
    #         if vault[key] == value:
    #             return vault['_id']
    
    # def get_by_id(self, id: str) -> VaultModel:
    #     raw_data = self.__get_raw_vaults()
        
    #     for vault in raw_data:
    #         if vault['_id'] == id:
    #             return VaultModel.model_validate(vault)

    # def get_one_where(self, key: str, value: str) -> VaultModel:
    #     raw_data = self.__get_raw_vaults()
        
    #     for vault in raw_data:
    #         if vault[key] == value:
                
    #             return VaultModel.model_validate(vault)

    # def get_all_where(self, key: str, value: str) -> list[VaultModel]:
    #     raw_data = self.__get_raw_vaults()
    #     vaults: list[VaultModel] = []
        
    #     for vault in raw_data:
    #         if vault[key] == value:
    #             vaults.append(VaultModel.model_validate(vault))
                
    #     return vaults

    # def update_one_where(self, data: VaultModel, key: str, value: str) -> bool:
    #     vault_id: str = self.get_id(key, value)
        
    #     if vault_id is None:
    #         raise ValueError('No updates could be performed as the ID could not be found.')
        
    #     original_vault: VaultModel = self.get_by_id(vault_id)
        
    #     if original_vault == data:
    #         raise ValueError('No updates have been made.')
        
    #     data.id = original_vault.id
    #     data.created = original_vault.created

    #     data_dump = data.model_dump(by_alias=True, mode='json')
            
    #     if self.is_test:
    #         update_file(test_db_name=self.db_name, data=data_dump, key=key, value=value, is_test=self.is_test, test_dir=self.test_dir)
    #     else:
    #         update_file(db_name=self.db_name, data=data_dump, key=key, value=value)
            
    #     raw_data = self.__get_raw_vaults()
        
    #     return data_dump in raw_data

    # def delete_one_where(self, key: str, value: str) -> bool:
    #     vault: VaultModel = self.get_one_where(key, value)
        
    #     if vault is None:
    #         raise LookupError('The vault could not be found.')
        
    #     data_dump = vault.model_dump(by_alias=True, mode='json')
        
    #     if self.is_test:
    #         update_file(test_db_name=self.db_name, data=None, key=key, value=value, is_test=self.is_test, test_dir=self.test_dir)
    #     else:
    #         update_file(db_name=self.db_name, data=None, key=key, value=value)
            
    #     raw_data = self.__get_raw_vaults()
        
    #     return data_dump not in raw_data

    # def delete_all_where(self, key: str, value: str) -> bool:
    #     vaults: list[VaultModel] = self.get_all_where(key, value)
        
    #     if len(vaults) == 0:
    #         raise LookupError('The vault could not be found.')
        
    #     data_dumps: list = [vault.model_dump(by_alias=True, mode='json') for vault in vaults]
        
    #     for _ in data_dumps:
    #         self.delete_one_where(key=key, value=value)
            
    #     raw_data: list[dict] = self.__get_raw_vaults()
    #     all_deleted: list[bool] = [vault not in raw_data for vault in data_dumps]
        
    #     return all(all_deleted)

    # def delete_database(self) -> bool:
    #     if self.is_test:
    #         return delete_file(test_db_name=self.db_name, is_test=self.is_test, test_dir=self.test_dir)
        
    #     else:
    #         return delete_file(db_name=self.db_name)
       