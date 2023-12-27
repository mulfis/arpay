# you have crazy enough to try cryptography? ok then
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import hashlib

# SHA-3 AREA
def encrypt_data(data, key):
    if data is None or key is None:
        raise ValueError("Data and key cannot be None for encryption.")
    
    # Pad the data before encryption
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    # Perform encryption
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return base64.urlsafe_b64encode(ciphertext).decode()

def decrypt_data(data, key):
    if data is None or key is None:
        raise ValueError("Data and key cannot be None for decryption.")

    # Perform base64 decoding
    decoded_data = base64.urlsafe_b64decode(data)

    # Perform decryption
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(decoded_data) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data.decode()

def derive_key(password):
    if password is None:
        raise ValueError("Password cannot be None for key derivation.")

    # Use SHA-3 directly for key derivation
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_256(),
        iterations=100000,
        salt=b'salt',
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    print(f'key: {key}')
    return key
# END OF AREA