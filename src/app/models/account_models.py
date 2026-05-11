'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Models for user account data
'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class AccountPasswordModel(BaseModel):
    salt: str
    hash: str

class AccountModel(BaseModel):
    _id: str
    name: str
    email: Optional[EmailStr]
    password: AccountPasswordModel
    created: datetime