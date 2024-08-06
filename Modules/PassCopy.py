import os
import pyperclip
import Modules.Utils as Utils
import Modules.CryptoFunctions as Crypto

def validarOpcion(opcion, totalPasswords, passwords):
    if opcion >= 0 and opcion <= totalPasswords:
        return passwords[opcion]
    else:
        print("Opción no válida. Intente de nuevo.")
        return None

def selectPassword():
    directorio = "Passwords/"
    passwords = []
    try:
        archivos = os.listdir(directorio)            
        for index, archivo in enumerate(archivos):
            print(f"{index} - {archivo}")
            passwords.append(archivo)

        totalPasswords = len(passwords) - 1
        while True:
            try:
                opcion = int(input(f"Elija una opción [0 - {totalPasswords}]: "))
                password_file = validarOpcion(opcion, totalPasswords, passwords)
                if password_file:
                    return password_file
            except ValueError:
                print("Por favor ingrese un número válido.")
    except FileNotFoundError:
        print(f"El directorio {directorio} no existe.")
        return None
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None

def main():
    tiempoEspera = 5
    password = selectPassword()
    while True:
        Utils.clearCli()
        if password is None:
            Utils.pausa(1)
        try:
            print(f"Archivo {password} actual")
            pin = Utils.tryPin()
            with open(f'Passwords/{password}', 'rb') as file:
                encrypted_password = file.read()
            decryptedPassword = Crypto.decryptPassword(encrypted_password, pin)
            if decryptedPassword:
                pyperclip.copy(decryptedPassword)
                print(f"Contraseña copiada al portapapeles. Se borrará en {tiempoEspera} segundos.")
                pyperclip.copy('')
                break
        except:
            print("Verifica el pin.")
            Utils.pausa(1)

if __name__ == "__main__":
    main()
