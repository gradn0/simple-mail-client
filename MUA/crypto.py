import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def deriveKey(salt):
    #derive encryption key from master password
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000,)
    return kdf.derive(bytes(os.environ.get("MASTER_PASS"), 'utf-8'))

def encrypt(password, key):
    #encrypt password
    aesgcm = AESGCM(key)
    nonce = bytes(os.urandom(12))
    
    return aesgcm.encrypt(nonce, password, None), nonce

def decrypt(ctpassword, key, nonce):

    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ctpassword, None)
