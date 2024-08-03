import os
import time


def clearCli():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausaInterrumpida():
    input("Presione Enter para continuar...")


def cerrarPrograma():
    opcion = input("¿Desea salir de la aplicación? [S/N] ")
    if opcion in ["S", "s"]:
        clearCli()
        return True
    clearCli()
    return False


def pausa(timer):
    time.sleep(timer)
