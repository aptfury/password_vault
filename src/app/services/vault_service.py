'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Service for the vault service.
'''

# ------------ imports ------------ #
from typing import Optional
from .auth_service import AuthService
from ..repositories import VaultRepo
from .session_service import SessionService
from ..configs import VaultModel, EntryModel

# ------------ class ------------ #
class VaultService:
    def __init__(self, session: SessionService, auth: AuthService, repository: VaultRepo):
        self.session: SessionService = session
        self.auth: AuthService = auth
        self.repo: VaultRepo = repository
        
    def logged_in(self) -> None:
        """Refuses user if user is not logged in

        Raises:
            PermissionError: You do not have permission for this operation. Please log back in and try again.
        """        
        if not self.auth.access_granted():
            raise PermissionError('You do not have permission for this operation. Please log back in and try again.')
        
        return
    
    def add_password(self, website: Optional[str], username: Optional[str], password: str) -> bool:
        """Adds the password the the user's vault.

        Args:
            website (Optional[str]): The url the login info is for
            username (Optional[str]): The username used to login
            password (str): The password to save

        Returns:
            bool: If the save was successful
        """    
        self.logged_in()
        
        entry: EntryModel = EntryModel(
            website=website,
            username=username,
            _password=password
        )    
        
        vault: VaultModel = self.repo.get('_id', self.session.id)
        vault.vault.append(entry)
        
        saved: bool = self.repo.update('_id', vault.id, vault)
        
        return saved
    
    def find_password(self, key: str, value: str) -> list[EntryModel]:
        """Finds stored password based on search criteria

        Args:
            key (str): The field to look at
            value (str): What should be stored in the field

        Returns:
            list[EntryModel]: A list of found stored passwords
        """            
        self.logged_in()
        
        vault: VaultModel = self.repo.get('_id', self.session.id)
        
        search_results: list[EntryModel] = []
        
        for entry in vault.vault:
            if getattr(entry, key) == value:
                search_results.append(entry)
            
        return search_results
    
    def view_passwords(self) -> list[EntryModel]:
        """Views all stored passwords.

        Returns:
            list[EntryModel]: A list of all stored passwords
        """        
        self.logged_in()
        
        vault: VaultModel = self.repo.get('_id', self.session.id)
        return vault.vault
    
    def edit_password(self, id: str, key: str, value: str) -> bool:
        """Edits a stored password

        Args:
            id (str): The id of the password
            key (str): The field to update
            value (str): The new value

        Returns:
            bool: If the stored password was saved successfully
        """        
        self.logged_in()
        
        vault: VaultModel = self.repo.get('_id', self.session.id)
        
        target: EntryModel = None

        for entry in vault.vault:
            if entry.id == id:
                target = entry
                break

        if target is None:
            return None
        
        vault.vault.remove(target)
        setattr(target, key, value)
        vault.vault.append(target)
        
        updated: bool = self.repo.update('_id', vault.id, vault)
        
        return updated
    
    def delete_password(self, id: str) -> bool:
        """Deletes a stored password.

        Args:
            id (str): The id of the password to delete.

        Returns:
            bool: If the password was deleted successfully.
        """        
        self.logged_in()
        
        vault: VaultModel = self.repo.get('_id', self.session.id)
        
        target: EntryModel = None
        
        for entry in vault.vault:
            if entry.id == id:
                target = entry
                break
            
        if target is None:
            return None
        
        vault.remove(target)
        
        deleted: bool = self.repo.update('_id', vault.id, vault)
        
        return deleted
    
    def delete_all_passwords(self) -> bool:
        """Deletes all stored passwords

        Returns:
            bool: If passwords were deleted successfully
        """        
        self.logged_in()
        
        vault: VaultModel = self.repo.get('_id', self.session.id)
        
        if vault.vault is None or vault.vault == []:
            return None
        
        vault.vault = []
        
        deleted: bool = self.repo.update('_id', vault.id, vault)
        return deleted
    
    def delete_vault(self, actor: str = 'system') -> bool:
        """Deletes an account's vault

        Returns:
            bool: If the vault was deleted successfully
        """    
        if actor == 'user':
            self.logged_in()
            
        deleted: bool = self.repo.delete('_id', self.session.id)
        return deleted