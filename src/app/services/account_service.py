'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Services for managing accounts
'''

# ------------ imports ------------ #
from .auth_service import AuthService
from ..repositories import AccountRepo
from .session_service import SessionService
from ..configs import AccountModel

# ------------ class ------------ #
class AccountService:
    def __init__(self, session: SessionService, auth: AuthService, repository: AccountRepo):
        self.session: SessionService = session
        self.auth: AuthService = auth
        self.repo: AccountRepo = repository

    def logged_in(self) -> None:
        '''Validates the user is logged in.'''
        if not self.auth.access_granted():
            raise PermissionError('You do not have permission for this operation. Please log in again.')
        
        return
        
    def view_account(self) -> str:
        '''Displays the non-protected user account information.'''
        
        self.logged_in()
        
        account: AccountModel = self.repo.get('_id', self.session.id) or None
        
        if account is None:
            return None, None, None
        
        return account.username, account.email, account.created
    
    def update_account(self, updates: dict) -> bool:
        """Updates account information based on user input

        Args:
            updates (dict): A dictionary of the updates, where the key is the attribute to update and the value is what it should be updated to.
        """        
        
        self.logged_in()
        
        account: AccountModel = self.repo.get('_id', self.session.id)
        changed: AccountModel = account.model_copy(deep=True)
        
        for key, value in updates.items():
            setattr(changed, key, value)
        
        if not account == changed:
            updated: bool = self.repo.update('_id', self.session.id, changed)
        
            self.session.username = changed.username

            return updated
        else:
            print('No changes made, update stopped.')
            return False
    
    def delete_account(self, actor: str = 'system') -> bool:
        """Deletes the user's account

        Args:
            actor (str, optional): Who is deleting the account. Defaults to 'system'.

        Returns:
            bool: If the account was successfully deleted
        """        
        if actor == 'user':
            self.logged_in()
            
        deleted: bool = self.repo.delete('_id', self.session.id)
        return deleted