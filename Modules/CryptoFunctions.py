import os
import subprocess
import sys
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def encriptarContrasena(password, pin):
    try:
        salt = os.urandom(16)
        key = sha256(pin.encode() + salt).digest()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                        backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        paddedPassword = padder.update(password.encode()) + padder.finalize()
        encryptedPassword = encryptor.update(
            paddedPassword) + encryptor.finalize()
        print("Contraseña encriptada")
        return salt + iv + encryptedPassword
    except Exception:
        print(f"Error al encriptar la contraseña")
        return None


def desencriptarContrasena(encryptedPassword, pin):
    try:
        salt = encryptedPassword[:16]
        encryptedPassword = encryptedPassword[16:]
        key = sha256(pin.encode() + salt).digest()
        iv = encryptedPassword[:16]
        encryptedPassword = encryptedPassword[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                        backend=default_backend())
        decryptor = cipher.decryptor()
        padded_password = decryptor.update(
            encryptedPassword) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        contrasena = unpadder.update(padded_password) + unpadder.finalize()
        print("Contraseña desencriptada")
        return contrasena.decode()
    except Exception:
        print(f"Error al desencriptar la contraseña")
        return None

