""" create_account.py

AUTHOR: blake lemarr
CREATED: 05.18.26
UPDATED: 05.18.26

DESCRIPTION:
    - the inputs for login
"""

# ------------ IMPORT ------------ #
from ...utilities import InputWithLabel

# ------------ INPUTS ------------ #
class LoginInputs:
    def username() -> InputWithLabel:
        return InputWithLabel(
            'USERNAME', 
            'exampleuser', 
            False
        )
    
    def password() -> InputWithLabel:
        return InputWithLabel(
            'PASSWORD', 
            '**********', 
            True
        )