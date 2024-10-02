import os
from Modules import Settings
import Modules.Utils as Utils

def leerArchivos(directorio):
    archivos = os.listdir(directorio)
    if not archivos:
        print("No hay contraseñas guardadas.")
        return []
    return archivos

def leerContrasenas(archivos):
    passwords = []
    for index, archivo in enumerate(archivos):
        print(f"{index+1} - {archivo}")
        passwords.append(archivo)
    return passwords

def selectPassword():
    Utils.pathVerificator()
    directorio = Settings.directory
    archivos = leerArchivos(directorio)

    if not archivos:
        return False

    passwords = leerContrasenas(archivos)
    totalPasswords = len(passwords)

    try:
        while True:
            try:
                opcion = int(input(f"Elija una opción [1 - {totalPasswords}]: "))
                if 1 <= opcion <= totalPasswords:
                    passwordFile = passwords[opcion - 1]
                    print(f"{passwordFile}")
                    return passwordFile
                else:
                    print("Opción fuera de rango. Intente de nuevo.")
            except ValueError:
                Utils.clearCli()
                print("Por favor ingrese un número válido.")
                return False
    except FileNotFoundError:
        print(f"El directorio {directorio} no existe.")
        return False
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return False

def main():
    Utils.clearCli()
    binFile = selectPassword()
    if not binFile:
        Utils.pausa(2)
    else:
        while True:
            Utils.clearCli()
            if Utils.recoverPassword(binFile):
                break

if __name__ == "__main__":
    main()
