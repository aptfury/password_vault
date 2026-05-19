""" create_account.py

AUTHOR: blake lemarr
CREATED: 05.18.26
UPDATED: 05.18.26

DESCRIPTION:
    - the buttons for log in
"""

# ------------ IMPORT ------------ #
import sys
from textual.widgets import Button
from textual.app import ComposeResult

# ------------ BUTTONS ------------ #
class CreateAccountSubmit:
    """Creates a submit button for the create account screen"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='submit',
            variant='success',
            name='create_account_submit',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        pass # todo - trigger create account
    
class CreateAccountBack:
    """Creates a back button for the create account screen"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='back',
            variant='default',
            name='create_account_back',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        pass # todo - trigger nav back
    
class CreateAccountExit:
    """Creates an exit button for the create account screen"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='exit',
            variant='error',
            name='create_account_exit',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        sys.exit(str(event.button))