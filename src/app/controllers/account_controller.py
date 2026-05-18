'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Interacts with user for account management
'''

# ------------ imports ------------ #
from ..configs import AccountModel, PasswordModel
from ..services import SessionService, AuthService, AccountService
from ..utilities import ScriptsUtilities

# ------------ class ------------ #
class AccountController:
    def __init__(self, session: SessionService, auth: AuthService, service: AccountService):
        self.session: SessionService = session
        self.auth: AuthService = auth
        self.service: AccountService = service
        self.scripts: ScriptsUtilities = ScriptsUtilities()

    def account_navigation(self):
        """Helps the user navigate through menu.
        """   
        self.service.logged_in()
        
        nav: list = ['1', '2', '3', '4', '9']
        
        self.scripts.account_menu(self.session.username)
        res: str = None
        
        for n in range(3):
            res = self.scripts.menu_option()
            
            if res in nav:
                break
            else:
                remaining: int = 3 - n
                print(f'[INVALID OPTION] {res} is not a valid menu option. (REMAINING ATTEMPTS: {remaining} of 3).')
                
                if remaining <= 0:
                    raise KeyError('[ACCOUNT_CONTROLLER_NAV] 3 invalid menu options in a row')
                
        if res == '1':
            # todo - update when system controller established
            pass
        elif res == '2':
            self.view_account()
        elif res == '3':
            self.update_account()
        elif res == '4':
            # todo - update when system controller established
            pass
        elif res == '9':
            # todo - update when system controller established
            self.delete_account()
    
    def view_account(self) -> None:
        """Returns a summary of user account info
        """        
        username, email, created = self.service.view_account()
        
        if any(username is None, email is None, created is None):
            print('User could not be found.')
            self.account_navigation()
        
        user_view: str = f'''
        ------------------------------------
                USER ACCOUNT DETAILS
        ------------------------------------
        
        USERNAME: {username}
        EMAIL: {email}
        CREATED: {created}
        '''
        
        print(user_view)
        
        print('Returning to account menu')
        
        self.account_navigation()

    def update_account(self) -> None:
        """Updates the user account
        """        
        print('Enter the new information in the field when prompted. Press enter to skip any information that you do not want to change.\n')
        
        username: str = input('NEW USERNAME: ')
        email: str = input('NEW EMAIL: ')
        password: str = input('NEW PASSWORD: ')
        
        changes: dict = {}
        
        if not username == '':
            changes['username'] = username
        if not email == '':
            changes['email'] = email
        if not password == '':
            new_pass: PasswordModel = self.auth.utils.hash_password(password)
            changes['password'] = new_pass
            
        success: bool = self.service.update_account(changes)
        
        if success:
            print('Account Updated!')
        else:
            print('Account could not be updated at this time.')
            
        self.account_navigation()

    def delete_account(self):
        """Deletes the user account from the database
        """     
        confirm: str = input('This action is permanent. Please type CONFIRM to complete this action: ')
        
        if not confirm == 'CONFIRM':
            print('Action terminated.')
            self.account_navigation()   
            
        else:
            deleted: bool = self.service.delete_account(actor='user')
            
            if not deleted:
                print('Account could not be deleted at this time.')
                self.account_navigation()
            else:
                return