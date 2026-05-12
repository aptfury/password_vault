'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Models for user vault data
'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class VaultEntryModel(BaseModel):
    id: str = Field(alias='_id')
    name: str
    website: Optional[str]
    username: Optional[str]
    password: str
    created: datetime
    
class VaultModel(BaseModel):
    user_id: str
    vault: list[VaultEntryModel]