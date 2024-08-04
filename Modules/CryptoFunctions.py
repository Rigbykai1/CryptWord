import os
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def encryptPassword(password, pin):
    key = sha256(pin.encode()).digest()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    paddedPassword = padder.update(password.encode()) + padder.finalize()
    encryptedPassword = encryptor.update(paddedPassword) + encryptor.finalize()
    return iv + encryptedPassword

def decryptPassword(encrypted_password, pin):
    key = sha256(pin.encode()).digest()
    iv = encrypted_password[:16]
    encrypted_password = encrypted_password[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_password = decryptor.update(encrypted_password) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    password = unpadder.update(padded_password) + unpadder.finalize()
    return password.decode()