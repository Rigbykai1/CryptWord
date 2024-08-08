import os
from Modules import Settings
import Modules.Utils as Utils


def selectPassword():
    Utils.pathVerificator()
    directorio = Settings.directory
    passwords = []
    archivos = os.listdir(directorio)
    if archivos == []:
        print("No hay contraseñas guardadas.")
        return False
    try:
        for index, archivo in enumerate(archivos):
            print(f"{index} - {archivo}")
            passwords.append(archivo)
        totalPasswords = len(passwords) - 1
        while True:
            try:
                opcion = int(
                    input(f"Elija una opción [0 - {totalPasswords}]: "))
                passwordFile = passwords[opcion]
                print(f"{passwordFile}")
                if passwordFile:
                    return passwordFile
            except Exception:
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
