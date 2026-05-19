'''
AUTHOR: Blake Lemarr
DATE: 05.18.26
DESCRIPTION: Contains the application scripts
'''

# ------------ imports ------------ #
import os
from functools import wraps

# ------------ utils ------------ #
class ScriptsUtilities:
    def __init__(self, ):
        self.dashes: str = '-----------------------------------------'
        self.dashes_length: int = len(self.dashes)
        
    def main_menu(self) -> None:
        script: list = [
            '-----------------------------------------',
            '                MAIN MENU                ',
            '-----------------------------------------',
            'Select an option from the menu below:    ',
            '(enter the # only; e.g.: 1)              ',
            '                                         ',
            '(1) Log In                               ',
            '(2) Create Account                       ',
            '(3) Exit                                 ',
            '-----------------------------------------'
        ]
        
        for line in script:
            print(line)
            
        return
        
    
    def account_menu(self, name: str) -> None:
        script: list = [
            '-----------------------------------------',
            '              ACCOUNT MENU               ',
            '-----------------------------------------',
            'Select an option from the meny below:    ',
            '(enter the # only; e.g.: 1)              ',
            '                                         ',
            '(1) Access Vault                         ',
            '(2) View Account                         ',
            '(3) Edit Account                         ',
            '(4) Log Out                              ',
            '-----------------------------------------',
            '           !!! D A N G E R !!!           ',
            '-----------------------------------------',
            '(0) Delete Account <- ALSO DELETES VAULT ',
            '-----------------------------------------'
        ]
        
        for line in script:
            print(line)
            
        return
    
    def vault_menu(self, name: str) -> None:
        script: list = [
            '-----------------------------------------',
            '               VAULT  MENU               ',
            '-----------------------------------------',
            'Select an option from the menu below:    ',
            '(enter the # only; e.g.: 1)              ',
            '                                         ',
            '(1) Add Password                         ',
            '(2) Find Password                        ',
            '(3) View All Passwords                   ',
            '(4) Manage Passwords                     ',
            '(5) Back                                 ',
            '(6) Log Out                              ',
            '-----------------------------------------',
            '           !!! D A N G E R !!!           ',
            '-----------------------------------------',
            '(0) Delete Vault <- ALSO DELETES ACCOUNT ',
            '-----------------------------------------'
        ]
        
        for line in script:
            print(line)
            
        return
        
    def password_manager_menu(self, name: str) -> None:
        script: list = [
            '-----------------------------------------',
            '              PASSWORD MENU              ',
            '-----------------------------------------',
            'Select an option from the menu below:    ',
            '(enter the # only; e.g.: 1)              ',
            '                                         ',
            '(1) Edit Password                        ',
            '(2) Delete Password                      ',
            '(3) Back                                 ',
            '(5) Log Out                              ',
            '-----------------------------------------',
            '           !!! D A N G E R !!!           ',
            '-----------------------------------------',
            '(0) Clear Vault / Delete All Passwords   ',
            '-----------------------------------------'
        ]
        
        for line in script:
            print(line)
            
        return        
        
    def menu_option(self) -> str:
        res: str = input('MENU OPTION: ')
        
        return res
    
    def custom_dash(self, l: int) -> str:
        return f'|{'-' * l}|'
    
    def custom_sides(self, l: int) -> str:
        return f'|{' ' * l}|'
    
    def custom_data(self, line: str, l: int) -> str:
        spaces: int = l - (len(line) - 1)
        return f'| {line}{' ' * spaces}|'
    
    def data_display(self, title: str, data: dict) -> str:
        length: int = len(title)
        title_length: int = self.dashes_length - (length + 6)
        title: str = f'----- {title} {'-' * title_length}-'
        
        template: list = [
            title
        ]
        
        for k, v in data.items():
            line: str = f'{k.upper()}: {v}'
            data_line: str = self.custom_data(line, length)
            template.append(data_line)
            
        template.append(self.custom_dash(length))