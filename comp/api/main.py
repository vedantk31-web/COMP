from fastapi import FastAPI
from auth import authenticate_user
from encryption import encrypt_message, decrypt_message
from crypto.Random import get_random_bytes

app = FastAPI()

@app.post("/authenticate")
def authenticate():
    # Authenticate the user
    user = authenticate_user()
    if user:
        return {"authenticated": True, "user": user}
    else:
        return {"authenticated": False, "message": "Authentication failed"}

@app.post("/encrypt")
def encrypt(message: str):
    # Generate a random key
    key = get_random_bytes(16)
    # Encrypt the message
    encrypted_message = encrypt_message(message, key)
    return {"encrypted_message": encrypted_message, "key": key}

@app.post("/decrypt")
def decrypt(encrypted_message: str, key: bytes):
    # Decrypt the message
    decrypted_message = decrypt_message(encrypted_message, key)
    return {"decrypted_message": decrypted_message}
