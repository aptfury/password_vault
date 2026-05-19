""" create_account.py

AUTHOR: blake lemarr
CREATED: 05.18.26
UPDATED: 05.18.26

DESCRIPTION:
    - custom form field widgets
"""

# ------------ IMPORT ------------ #
from textual.widget import Widget
from textual.app import ComposeResult
from textual.widgets import Input, Label

# ------------ FIELD ------------ #
class InputWithLabel(Widget):
    """A field input with a label and placeholder."""
    
    DEFAULT_CSS = """
    InputWithLabel {
        layout: horizontal;
        height: auto;
    }
    InputWithLabel Label {
        padding: 1;
        width: 12;
        text-align: right;
    }
    InputWithLabel Input {
        width: 1fr;
    }
    """
    
    def __init__(self, input_label: str, input_placeholder: str, password: bool = False) -> None:
        self.input_label = input_label
        self.input_placeholder = input_placeholder
        self.input_password = password
        super().__init__()
        
    def compose(self) -> ComposeResult:
        yield Label(
            self.input_label
        )
        yield Input(
            placeholder=self.input_placeholder,
            password=self.input_password
        )