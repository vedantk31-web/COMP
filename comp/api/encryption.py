# encryption.py
from crypto.Cipher import AES
from crypto.Random import get_random_bytes
import base64

def encrypt_message(message, key):
    """Encrypts a message using AES encryption."""
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_message(encrypted_message, key):
    """Decrypts an AES encrypted message."""
    encrypted_message_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
    nonce = encrypted_message_bytes[:16]
    ciphertext = encrypted_message_bytes[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode('utf-8')
