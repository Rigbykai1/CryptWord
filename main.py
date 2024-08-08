import Modules.PassCopy as PassCopy
import Modules.PassWordEncripter as PassWordEncripter
import Modules.PasswordGen as PasswordGen
import Modules.Utils as Utils
import Modules.Settings as Settings
import time


def selectOption():
    print("1. Cifrar contraseña")
    print("2. Descifrar contraseña")
    print("3. Generar contraseña")
    print("4. Configuración")
    print("5. Salir")
    option = input("Elija una opción: ")
    return option


def options():
    Utils.clearCli()
    menuOption = selectOption()
    Utils.clearCli()
    if menuOption == "5":
        return False
    elif menuOption == "1":
        PassWordEncripter.main()
    elif menuOption == "2":
        PassCopy.main()
    elif menuOption == "3":
        PasswordGen.main()
    elif menuOption == "4":
        Settings.main()
    else:
        print("Opción no válida. Intente de nuevo.")
    time.sleep(1)
    Utils.clearCli()
    return True


def main():
    while True:
        option = options()
        if not option:
            Utils.clearCli()
            print("Saliendo de CryptWord")
            Utils.pausa(2)
            break
        else:
            if Utils.cerrarPrograma():
                break
        Utils.clearCli()


if __name__ == "__main__":
    main()
