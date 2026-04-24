import base64

from cryptography.fernet import Fernet


def encrypt(text: str, key: str) -> str:
    key_bytes = key.encode().ljust(32, b'0')[:32]
    key_b64 = base64.urlsafe_b64encode(key_bytes)
    cipher = Fernet(key_b64)
    return cipher.encrypt(text.encode()).decode()


def decrypt(encrypted: str, key: str) -> str:
    key_bytes = key.encode().ljust(32, b'0')[:32]
    key_b64 = base64.urlsafe_b64encode(key_bytes)
    cipher = Fernet(key_b64)
    return cipher.decrypt(encrypted.encode()).decode()
