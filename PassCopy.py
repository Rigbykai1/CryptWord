import os
import pyperclip
import getpass
import Utils
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from hashlib import sha256


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


def selectPassword():
    directorio = "Passwords/"
    passwords = []
    try:
        archivos = os.listdir(directorio)
        for index, archivo in enumerate(archivos):
            print(f"{index} - {archivo}")
            passwords.append(archivo)

        totalPasswords = len(passwords) - 1
        opcion = int(input(f"Elija una opción [0 - {totalPasswords}]: "))

        if opcion >= 0 and opcion <= totalPasswords:
            return passwords[opcion]
        else:
            print("Opción no válida. Intente de nuevo.")
    except FileNotFoundError:
        print(f"El directorio {directorio} no existe.")
    except ValueError:
        print("Entrada no válida. Por favor ingrese un número.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


def main():
    tiempo_espera = 5
    while True:
        fileName = selectPassword()
        pin_usuario = getpass.getpass(prompt="Ingresa el PIN: ")

        try:
            with open(f'Passwords/{fileName}', 'rb') as file:
                encrypted_password = file.read()
            decrypted_password = decrypt_password(
                encrypted_password, pin_usuario)
            if decrypted_password:
                pyperclip.copy(decrypted_password)
                print(f"Contraseña copiada al portapapeles. Se borrará en {
                      tiempo_espera} segundos.")
                Utils.pausa(tiempo_espera)
                pyperclip.copy('')
                break
            else:
                print("PIN incorrecto. Inténtalo nuevamente.")
                Utils.pausa(tiempo_espera)
                Utils.clearCli()

        except Exception as e:
            print(f"Error al descifrar: {e}, intente de nuevo")
            Utils.pausa(tiempo_espera)
            Utils.clearCli()


if __name__ == "__main__":
    main()
