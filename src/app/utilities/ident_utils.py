'''
AUTHOR: Blake Lemarr
DATE: 05.12.26
DESCRIPTION: Hands generation of IDs throughout the application.
'''

# ------------ IMPORTS ------------ #
import time
import string
import secrets

from datetime import datetime
from typing import NewType

# ------------ CUSTOM TYPES ------------ #

SecureID = NewType('SecureID', str)
LookupID = NewType('LookupID', str)
NanoID = NewType('NanoID', str)
TraceID = NewType('TraceID', str)

# ------------ IDENTIFICATION ------------ #
class IdentUtils:
    
    signature: list[str] = [secrets.token_bytes(2).hex() for _ in range(5)]
    
    def __init__(self):
        pass

    def __format_uuid(self, h: hex) -> str:
        return f'{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}'
    
    def __time_in_ms(self, as_bytes: bool = True) -> bytes | int:
        ns: int = time.time_ns()
        ms: int = ns // 1_000_000
        
        if as_bytes:
            return ms.to_bytes(6, byteorder='big')
        else:
            return ms
        
    def generate_secure_id(self) -> SecureID:
        raw: bytes = bytearray(secrets.token_bytes(16))
        
        # adjust to uuidv4
        raw[6] = (raw[6] & 0x0f) | 0x40
        raw[8] = (raw[8] & 0x3f) | 0x80
        
        h: hex = raw.hex()
        
        return SecureID(self.__format_uuid(h))
    
    def generate_lookup_id(self) -> LookupID:
        # timestamp
        time: bytes = self.__time_in_ms()
        
        # bytearray
        raw: bytes = bytearray(time + secrets.token_bytes(10))
        
        # adjust to uuidv7
        raw[6] = (raw[6] & 0x0f) | 0x70
        raw[8] = (raw[8] & 0x3f) | 0x80
        
        h: hex = raw.hex()
        
        return LookupID(self.__format_uuid(h))
    
    def generate_trace_id(self) -> TraceID:
        alphabet: str = string.ascii_letters + string.digits
        trace_id: str = ''
        
        time: str = datetime.now().strftime("%Y%m%d%H%M%S")
        trace_id += f'{time}_t'
        
        for _ in range(12):
            trace_id += secrets.choice(alphabet)
        
        return TraceID(trace_id)
    
    def generate_nano_id(self) -> NanoID:
        alphabet: str = string.ascii_letters + string.digits
        nano_id: str = ''
        
        for _ in range(12):
            nano_id += secrets.choice(alphabet)
            
        nano_id += secrets.choice(self.signature)
            
        return NanoID(nano_id)
    
    def id_type(self, id: str) -> str:
        lengths: dict = {
            36: 'uuid',
            28: 'trace_id',
            16: 'nano_id'
        }
        
        return lengths[len(id)]
    
    def verify_uuid(self, id: str, id_type: str = 'secure') -> bool:
        if len(id) != 36:
            return False
        
        versions: dict = {
            'secure': '4',
            'lookup': '7'
        }
        variance: str = '89ab'
        version: string = versions.get(id_type)
        
        try:
            is_valid = (
                id[14] == version and
                id[19].lower() in variance and
                id.count('-') == 4
            )
            return is_valid
        except IndexError:
            return False
        
    def verify_trace_id(self, id: str) -> bool:
        if len(id) != 28:
            return False
        
        try:
            is_valid = (
                id[15] == 't' and
                id[14] == '_' and
                all(n.isdigit() for n in id[:14])
            )
            return is_valid
        except IndexError:
            return False
        
    def verify_nano_id(self, id: str) -> bool:
        if len(id) != 16:
            return False
        
        try:
            return id[12:16] in self.signature
        except IndexError:
            return False