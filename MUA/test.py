import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives.ciphers.aead import AESGCM



def deriveKey(mpassword, salt):
    #derive encryption key from master password
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000,)
    return kdf.derive(mpassword)

def encrypt(password, salt):
    key = deriveKey(bytes(os.environ.get("MASTER_PASS"), 'utf-8'), salt)

    #encrypt password
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    return aesgcm.encrypt(nonce, password, None), nonce

def decrypt(ctpassword, salt, nonce):
    key = deriveKey(os.environ.get("MASTER_PASS"), salt)

    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ctpassword, None)





