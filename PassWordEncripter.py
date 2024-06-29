import os
import time
import getpass
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def encrypt_password(password, pin):
    key = sha256(pin.encode()).digest()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_password = padder.update(password.encode()) + padder.finalize()
    encrypted_password = encryptor.update(
        padded_password) + encryptor.finalize()
    return iv + encrypted_password


def decrypt_password(encrypted_password, pin):
    key = sha256(pin.encode()).digest()
    iv = encrypted_password[:16]
    encrypted_password = encrypted_password[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    padded_password = decryptor.update(
        encrypted_password) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    password = unpadder.update(padded_password) + unpadder.finalize()
    return password.decode()


tiempo_espera = 5
password = input("Ingresa la contraseña a cifrar: ")
wrongPin = False
while True:
    if wrongPin == True:
        print("Pines distintos. Intente nuevamente.")
        wrongPin = False

    pin = getpass.getpass(prompt="Ingresa el PIN de cifrado: ")
    verifiedPin = getpass.getpass(prompt="Confirma el PIN de cifrado: ")
    if pin == verifiedPin:
        clear_console()
        break
    wrongPin = True
    clear_console()

fileName = input("Ingresa un nombre para el archivo: ")

encrypted_password = encrypt_password(password, pin)

with open(f'{fileName}.bin', 'wb') as file:
    file.write(encrypted_password)
    print("Contraseña cifrada guardada en tus archivos :D.")
    print(f"La aplicación cerrará en {tiempo_espera}s")
    time.sleep(tiempo_espera)
