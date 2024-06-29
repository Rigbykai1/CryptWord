import pyperclip
import time
import getpass
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from hashlib import sha256


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


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

while True:
    fileName = input("Ingresa el nombre del archivo: ")
    pin_usuario = getpass.getpass(prompt="Ingresa el PIN: ")

    try:
        with open(f'{fileName}.bin', 'rb') as file:
            encrypted_password = file.read()
        decrypted_password = decrypt_password(encrypted_password, pin_usuario)

        if decrypted_password:
            pyperclip.copy(decrypted_password)
            print(f"Contraseña copiada al portapapeles. Se borrará en {
                  tiempo_espera} segundos.")
            time.sleep(tiempo_espera)
            pyperclip.copy('')
            break
        else:
            print("PIN incorrecto. Inténtalo nuevamente.")
            time.sleep(2)
            clear_console()

    except Exception as e:
        print(f"Error al descifrar: {e}")
        print(f"Cerrando script. Se cerrará en {2} segundos.")
        time.sleep(2)
        clear_console()
