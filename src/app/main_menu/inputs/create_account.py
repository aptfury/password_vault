""" create_account.py

AUTHOR: blake lemarr
CREATED: 05.18.26
UPDATED: 05.18.26

DESCRIPTION:
    - the inputs for account creations
"""

# ------------ IMPORT ------------ #
from ...utilities import InputWithLabel

# ------------ INPUTS ------------ #
class CreateAccountInputs:
    def username() -> InputWithLabel:
        return InputWithLabel(
            'USERNAME',
            'exampleusername',
            False
        )
        
    def password() -> InputWithLabel:
        return InputWithLabel(
            'PASSWORD',
            '**********',
            True
        )
        
    def re_enter_password() -> InputWithLabel:
        return InputWithLabel(
            'RE-ENTER PASSWORD',
            '**********',
            True
        )
        
    def email() -> InputWithLabel:
        return InputWithLabel(
            'EMAIL',
            'username@example.com',
            False
        )