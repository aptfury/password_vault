""" log_in.py

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
class LogInSubmit:
    """Creates a submit button for the log in screen"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='submit',
            variant='success',
            name='log_in_submit',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        pass # todo - trigger login
    
class LogInBack:
    """Creates a back button for the log in screen"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='back',
            variant='default',
            name='log_in_back',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        pass # todo - trigger nav back
    
class LogInExit:
    """Creates an exit button for the log in screen"""
    
    CSS_PATH = ''
    
    def compose(self) -> ComposeResult:
        yield Button(
            label='exit',
            variant='error',
            name='log_in_exit',
            flat=True
        )
        
    def on_button_pressed(self, event: Button.Pressed):
        sys.exit(str(event.button))