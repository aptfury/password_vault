'''
AUTHOR: Blake Lemarr
DATE: 05.11.26
DESCRIPTION: Models for user vault data
'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class VaultEntryModel(BaseModel):
    _id: str
    name: str
    website: Optional[str]
    username: Optional[str]
    password: str
    
class VaultModel(BaseModel):
    user_id: str
    vault: list[VaultEntryModel]