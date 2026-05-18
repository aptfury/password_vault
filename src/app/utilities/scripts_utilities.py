'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Contains the application scripts
'''

# ------------ imports ------------ #


# ------------ class ------------ #
class ScriptsUtilities:
    def main_menu(self) -> None:
        script: str = '''
        -------------------------
                MAIN MENU
        -------------------------
        
        Welcome to Password Vault!!
        
        Select an option from the menu below:
        
        (1) Log In
        (2) Create Account
        (3) Exit
        '''
        
        print(script)
    
    def account_menu(self, name: str) -> None:
        script: str = f'''
        ----------------------------
                ACCOUNT MENU
        ----------------------------
        
        Welcome back, {name}!
        
        Select an option from the menu below:
        
        (1) Access Password Vault
        (2) View Account
        (3) Edit Account
        (4) Delete Account
        (5) Log Out
        '''
        
        print(script)
    
    def vault_menu(self, name: str) -> None:
        script: str = f'''
        --------------------------
                VAULT MENU
        --------------------------
        
        {name}'s Vault
        
        Select an option from the menu below:
        
        (1) Add Password
        (2) Find Password
        (3) View All Passwords
        (4) Manage Passwords
        (5) Return to Account Menu
        (6) Log Out
        
        -- DANGER --
        (9) Delete Vault
        '''
        
        print(script)
        
    def password_manager_menu(self) -> None:
        script: str = '''
        -------------------------------------
                PASSWORD MANAGER MENU
        -------------------------------------
        
        Select an option from the menu below:
        
        (1) Edit Password
        (2) Delete Password
        (3) Return to Vault Menu
        (4) Return to Account Menu
        (5) Log Out
        
        -- DANGER --
        (9) Delete All Passwords - Will not delete vault
        '''
        
        print(script)
        
    def menu_option(self) -> str:
        res: str = input('''
        MENU OPTION (#): ''')
        
        return res