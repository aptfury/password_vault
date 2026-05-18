'''
AUTHOR: Blake Lemarr
DATE: 05.17.26
DESCRIPTION: Session manager
'''

# ------------ imports ------------ #

# ------------ class ------------ #
class SessionService:
    def __init__(self):
        self.session_id: str = None
        self.id: str = None
        self.username: str = None
        
    def login(self, key: str, id: str, username: str):
        self.session_id = key
        self.id = id
        self.username = username
        
        return
    
    def logout(self):
        self.session_id = None
        self.id = None
        self.username = None
        
        return