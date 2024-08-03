import os
import getpass
import Utils
from hashlib import sha256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def encrypt_password(password, pin):
    key = sha256(pin.encode()).digest()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    paddedPassword = padder.update(password.encode()) + padder.finalize()
    encryptedPassword = encryptor.update(paddedPassword) + encryptor.finalize()
    return iv + encryptedPassword


def main():
    wrongPin = False

    password = input("Ingresa la contraseña a cifrar: ")

    while True:
        if wrongPin:
            print("Pines distintos. Intente nuevamente.")
            wrongPin = False

        pin = getpass.getpass(prompt="Ingresa el PIN de cifrado: ")
        verifiedPin = getpass.getpass(prompt="Confirma el PIN de cifrado: ")
        if pin == verifiedPin:
            Utils.clearCli()
            break
        wrongPin = True
        Utils.clearCli()

    fileName = input("Ingresa un nombre para el archivo: ")

    encryptedPassword = encrypt_password(password, pin)

    with open(f'Passwords/{fileName}.bin', 'wb') as file:
        file.write(encryptedPassword)
        print("Contraseña cifrada guardada en tus archivos :D.")


if __name__ == "__main__":
    main()
