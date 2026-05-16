'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: The main file for the program that interacts
             with the user and helps them navigate the application.
'''

# ------------ IMPORTS ------------ #
import sys

from app.services.account_service import AccountService

# ------------ MAIN ------------ #
def main():
    accounts: AccountService = AccountService()
    welcome_message = '''
------------------------------------------
        WELCOME TO PASSWORD VAULT!    
------------------------------------------
Select an option to get started:

(1) Create Account
(2) Log In
(3) Exit
'''
    print(welcome_message)
    
    selection: str = input('Enter a number: ')
    
    if selection == '1':
        accounts.create_account()
        return main()
    
    elif selection == '2':
        res: str | None = accounts.account_menu()
        
        if res == 'log out':
            res = None
            return main()
    
    elif selection == '3':
        print('\nThanks for stopping by!')
        return sys.exit()
    
    else:
        print(f'INVALID OPTION: {selection}')
        
        back_to_main: str = input('Return to main menu [y/n]?: ')
        
        if back_to_main == 'y':
            return main()
        else:
            print('\nSession aborted.')
            return sys.exit()

main()