'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Interacts with user for account management
'''

# ------------ imports ------------ #
from ..configs import VaultModel, EntryModel
from ..services import SessionService, AuthService, VaultService
from ..utilities import ScriptsUtilities

# ------------ class ------------ #
class VaultController:
    def __init__(self, session: SessionService, auth: AuthService, service: VaultService):
        self.session: SessionService = session
        self.auth: AuthService = auth
        self.service: VaultService = service
        self.scripts: ScriptsUtilities = ScriptsUtilities()

    def vault_navigation(self):
        """Helps the user navigate through menu.
        """   
        self.service.logged_in()
        
        nav: list = ['1', '2', '3', '4', '5', '6', '9']
        
        self.scripts.vault_menu(self.session.username)
        res: str = None
        
        for n in range(3):
            res = self.scripts.menu_option()
            
            if res in nav:
                break
            else:
                remaining: int = 3 - n
                print(f'[INVALID OPTION] {res} is not a valid menu option. (REMAINING ATTEMPTS: {remaining} of 3).')
                
                if remaining <= 0:
                    raise KeyError('[VAULT_CONTROLLER_NAV] 3 invalid menu options in a row')
                
        if res == '1':
            self.add_password()
        elif res == '2':
            self.find_password()
        elif res == '3':
            self.view_passwords()
        elif res == '4':
            self.password_navigation()
        elif res == '5':
            # todo - update when system controller established
            pass
        elif res == '6':
            # todo - update when system controller established
            pass
        elif res == '9':
            # todo - update when system controller established
            pass
    
    def password_navigation(self):
        """Helps the user navigate through menu.
        """   
        self.service.logged_in()
        
        nav: list = ['1', '2', '3', '4', '5', '9']
        
        self.scripts.password_manager_menu(self.session.username)
        res: str = None
        
        for n in range(3):
            res = self.scripts.menu_option()
            
            if res in nav:
                break
            else:
                remaining: int = 3 - n
                print(f'[INVALID OPTION] {res} is not a valid menu option. (REMAINING ATTEMPTS: {remaining} of 3).')
                
                if remaining <= 0:
                    raise KeyError('[VAULT_CONTROLLER_NAV] 3 invalid menu options in a row')
                
        if res == '1':
            self.edit_password()
        elif res == '2':
            self.delete_password()
        elif res == '3':
            self.vault_navigation()
        elif res == '4':
            # todo - update when system controller established
            pass
        elif res == '5':
            # todo - update when system controller established
            pass
        elif res == '9':
            self.delete_all_passwords()
        
    def add_password(self):
        """Creates a stored password
        """        
        print('Enter the following information as prompted. You can press enter to skip website and username if desired.')
        
        website: str = input('ENTER WEBSITE: ')
        username: str = input('ENTER USERNAME: ')
        password: str = input('ENTER PASSWORD: ')
        
        success: bool = self.service.add_password(website, username, password)
        
        if success:
            print('Password Stored!')
            print('\n[WARNING!!!] If you did not add a website or username, you will have to find your idea by viewing all passwords if you want to make any changes.\n')
        else:
            print('Password could not be stored.')
            
        self.vault_navigation()
    
    def find_password(self):
        """Finds stored passwords by search criteria.
        """        
        key: str = ''
        keys: list = ['id', 'website', 'username']
        
        for k in keys:
            res: str = input(f'Search passwords by {k} (y/n)?:')
            
            if res.lower() == 'y':
                key = k
                break

        if key == '':
            print('Valid key not chosen.')
            self.vault_navigation()
            
        value: str = input(f'Find for {key}: ')
        
        res: list[EntryModel] = self.service.find_password(key, value)
        
        if len(res) == 0:
            print('No passwords found.')
            self.vault_navigation()
            
        show: str = input(f'Reveal passwords (y/n)?: ')
        
        for entry in res:
            template: str = f'''
            -------------------------------
                    RESULTS: {res.index(entry) + 1} of {len(res)}
            -------------------------------
            ID: {entry.id}
            WEBSITE: {entry.website}
            USERNAME: {entry.username}
            PASSWORD: {entry.password if show == 'y' else entry.protected_password}
            '''
        
        self.vault_navigation()
    
    def view_passwords(self):
        """Shows all passwords
        """   
        stored: list[EntryModel] = self.service.view_passwords()
        
        if len(stored) == 0:
            print('No passwords found.')
            self.vault_navigation()
            
        show: str = input('Reveal passwords (y/n)?: ')
        
        for entry in stored:
            template: str = f'''
            -------------------------------
                    RESULTS: {stored.index(entry) + 1} of {len(stored)}
            -------------------------------
            ID: {entry.id}
            WEBSITE: {entry.website}
            USERNAME: {entry.username}
            PASSWORD: {entry.password if show == 'y' else entry.protected_password}
            '''   
            
        self.vault_navigation()
    
    def edit_password(self):
        pass
    
    def delete_password(self):
        pass
    
    def delete_all_passwords(self):
        pass
    
    def delete_vault(self):
        pass