""" create_account.py

AUTHOR: blake lemarr
CREATED: 05.18.26
UPDATED: 05.18.26

DESCRIPTION:
    - the buttons for main menu
"""

# ------------ IMPORT ------------ #
import sys
from textual.widgets import Button
from textual.app import ComposeResult

# ------------ BUTTONS ------------ #
class MainMenuCreateAccount:
    """Creates the create account button on the main menu"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='create account',
            variant='default',
            name='main_menu_create_account',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        pass # todo - trigger create account screen
    
class MainMenuLogIn:
    """Creates the log in button on the main menu"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='log in',
            variant='primary',
            name='main_menu_log_in',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        pass # todo - trigger log in screen
    
class MainMenuExit:
    """Creates the exit button on the main menu"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='exit',
            variant='error',
            name='main_menu_exit',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        sys.exit(str(event.button))