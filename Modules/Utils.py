import os
import time
import getpass


def clearCli():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa(timer):
    time.sleep(timer)

def pausaInterrumpida():
    input("Presione Enter para continuar...")


def cerrarPrograma():
    opcion = input("¿Desea salir de la aplicación? [S/N] ")
    if opcion in ["S", "s"]:
        clearCli()
        return True
    clearCli()
    return False

def tryPin():
    pin = getpass.getpass(prompt="Ingresa el PIN: ")  
    return pin

def verifyPin():
    while True:
        pin1 = getpass.getpass(prompt="Ingresa el PIN: ")  
        pin2 = getpass.getpass(prompt="Confirme el PIN: ")
        if pin1 == pin2:
            print('\nLos pines ingresados coinciden\n')
            pausa(1)
            return pin1
        else:
            print('\nPines distintos, intenta nuevamente.\n')
            pausa(1)
            clearCli()