'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Models for user vault data
'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class VaultLoginDataModel(BaseModel):
    username: Optional[str]
    password: str

class VaultEntryModel(BaseModel):
    id: str = Field(alias='_id')
    name: Optional[str]
    website: Optional[str]
    login: VaultLoginDataModel
    created: datetime
    
class VaultModel(BaseModel):
    id: str = Field(alias='_id')
    user_id: str
    created: datetime
    vault: list[VaultEntryModel]