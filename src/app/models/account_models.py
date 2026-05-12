'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Models for user account data
'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class AccountPasswordModel(BaseModel):
    salt: str
    hash: str

class AccountModel(BaseModel):
    id: str = Field(alias='_id')
    name: str
    email: Optional[EmailStr]
    password: AccountPasswordModel
    created: datetime