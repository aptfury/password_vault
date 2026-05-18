'''
AUTHOR: Blake Lemarr
DATE: 05.16.26
DESCRIPTION: The user account models
'''

# ------------ imports ------------ #
import string
import secrets
from uuid import uuid4
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, computed_field

# ------------ helpers ------------ #
def nano_id() -> str:
    alphabet: str = string.digits
    nano_id: str = ''
    for _ in range(18):
        nano_id += secrets.choice(alphabet)
        
    return nano_id

# ------------ account ------------ #
class AccountModel(BaseModel):
    id: str = Field(alias='_id', default_factory=lambda: str(uuid4()))
    username: str
    email: Optional[EmailStr]
    password: PasswordModel
    created: datetime = Field(default_factory=lambda: datetime.now())
    
    @computed_field
    @property
    def protected_email(self) -> str:
        return self.email[:3] + ('*' * (len(self.email) - 3))
    
# ------------ account::password ------------ #
class PasswordModel(BaseModel):
    salt: str
    hashed: str

# ------------ vault ------------ #
class VaultModel(BaseModel):
    id: str = Field(alias='_id')
    salt: str
    vault: list[EntryModel] = Field(default=[])

# ------------ vault::entry ------------ #
class EntryModel(BaseModel):
    id: str = Field(alias='_id', default_factory=lambda: nano_id())
    website: Optional[str]
    username: Optional[str]
    password: str = Field(alias='_password')
    created: datetime = Field(default_factory=lambda: datetime.now())
    
    @computed_field
    @property
    def protected_password(self) -> str:
        return ['*' * len(self.password)]
