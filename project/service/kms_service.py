from datetime import date
import hashlib, hmac, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from model.customer_pii import CustomerPII, TaxIdType

def generate_blind_index(key_mac, data):
    return hmac.new(key_mac, data, hashlib.sha256).digest()

def encrypt(data, key_enc, integrity_context):
    aesgcm = AESGCM(key_enc)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data,integrity_context)
    return nonce + ciphertext

def decrypt(payload, key_enc, integrity_context):
    aesgcm = AESGCM(key_enc)
    nonce = payload[:12]
    ciphertext = payload[12:]
    return aesgcm.decrypt(nonce, ciphertext, integrity_context)

data = "123.456.789-01".encode()    # str -> bytes
key_enc = os.urandom(32)            # AES-256 
key_mac = os.urandom(32)            # HMAC
aad = "user_123".encode()           # Additional Authenticated Data (AAD)

email = "email@example.com".encode()
phone = "879123456789".encode()
name = "John Doe".encode()
date_of_birth = date(2003, 8, 29)

generate_blind_index(key_mac, data)
payload = encrypt(data, key_enc, aad)
decrypt(payload, key_enc, aad)
