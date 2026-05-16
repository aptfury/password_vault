'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Models for user account data
'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class AccountAuthModel(BaseModel):
    auth_salt: str
    auth_hash: str
    vault_id: Optional[str]
    vault_salt: Optional[str]

class AccountModel(BaseModel):
    id: str = Field(alias='_id')
    name: str
    email: Optional[EmailStr]
    password: AccountAuthModel
    created: datetime