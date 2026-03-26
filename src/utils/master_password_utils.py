import bcrypt
from hashlib import sha256

def encrypt_password(password):
    pepper = 'masterpepper'.encode()
    salt = bcrypt.gensalt()
    peppered: bytes = f'{password}-{pepper}'.encode()
    hashed: bytes = bcrypt.hashpw(peppered, salt)

