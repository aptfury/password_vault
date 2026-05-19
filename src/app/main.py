''' main.py

AUTHOR: blake lemarr
CREATED: 05.18.26
UPDATED: 05.18.26

DESCRIPTION:
    - the main application
'''

# ------------ IMPORTS ------------ #
from textual.app import App

# ------------ APPLICATION ------------ #
class PasswordVault(App):
    pass

if __name__ == '__main__':
    app: App = PasswordVault()
    app.run()