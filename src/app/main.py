'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: The main script.
'''

# ------------ imports ------------ #
from .services import AuthService
from .services import SessionService

# ------------ class ------------ #
def main():
    session: SessionService = SessionService()
    auth: AuthService = AuthService(session=session)

main()