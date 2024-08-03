import PassCopy
import PassWordEncripter
import Utils
import time


def main():
    while True:
        print("1. Cifrar contraseña")
        print("2. Descifrar contraseña")
        print("3. Salir")
        opcion = input("Elija una opción: ")
        if opcion == "1":
            Utils.clearCli()
            PassWordEncripter.main()
            if Utils.cerrarPrograma():
                break
        elif opcion == "2":
            Utils.clearCli()
            PassCopy.main()
            if Utils.cerrarPrograma():
                break
        elif opcion == "3":
            Utils.clearCli()
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            time.sleep(2)
            Utils.clearCli()


if __name__ == "__main__":
    main()
