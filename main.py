import Modules.PassCopy as PassCopy
import Modules.PassWordEncripter as PassWordEncripter
import Modules.PasswordGen as PasswordGen
import Modules.Utils as Utils
import time

def selectOption():
    print("1. Cifrar contraseña")
    print("2. Descifrar contraseña")
    print("3. Generar contraseña")
    print("4. Salir")
    option = input("Elija una opción: ")
    return option

def options(menuOption):
    Utils.clearCli()
    if menuOption == "4":
        Utils.clearCli()
        return False
    elif menuOption == "1":
        PassWordEncripter.main()
    elif menuOption == "2":
        PassCopy.main()
    elif menuOption == "3":
        PasswordGen.main()
    else:
        print("Opción no válida. Intente de nuevo.")
        time.sleep(1)
        return False
    time.sleep(2)
    Utils.clearCli()
    return True

def main():
    while True:
        option = selectOption()
        if options(option):
            if Utils.cerrarPrograma():
                break
        Utils.clearCli()
        

if __name__ == "__main__":
    main()
