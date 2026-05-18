'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Services for managing accounts
'''

# ------------ imports ------------ #
from .auth_service import AuthService
from ..repositories import AccountRepo
from .session_service import SessionService
from ..configs.models import AccountModel, PasswordModel

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
        
    def view_account(self) -> None:
        '''Displays the non-protected user account information.'''
        
        self.logged_in()
        
        account: AccountModel = self.repo.get('_id', self.session.id)
        
        user_view: str = f'''
        ------------------------------------
                USER ACCOUNT DETAILS
        ------------------------------------
        
        USERNAME: {account.username}
        EMAIL: {account.email}
        CREATED: {account.created}
        '''
        
        print(user_view)
        
        return
    
    def update_account(self, updates: dict) -> None:
        """Updates account information based on user input

        Args:
            updates (dict): A dictionary of the updates, where the key is the attribute to update and the value is what it should be updated to.
        """        
        
        self.logged_in()
        
        account: AccountModel = self.repo.get('_id', self.session.id)
        changed: AccountModel = account.model_copy(deep=True)
        
        for key, value in updates.items():
            if key == '_id':
                print('User id cannot be changed.')
                
            if key == 'created':
                print('Account creation date cannot be changed.')
            
            if not key == '_id' and not key == 'created':
                setattr(changed, key, value)
        
        if not account == changed:
            updated: bool = self.repo.update('_id', self.session.id, changed)
        
            if updated:
                self.session.username = changed.username
                print('UPDATE SUCCESSFUL!')
                
        else:
            print('No changes were made, update cancelled.')
            
        return