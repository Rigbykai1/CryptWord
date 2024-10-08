import os
import time
import getpass
import pyperclip
import Modules.CryptoFunctions as Crypto
from Modules import Settings


def pathVerificator():
    if not os.path.exists(Settings.folderName):
        os.makedirs(Settings.folderName)


def clearCli():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa(timer):
    time.sleep(timer)


def pausaInterrumpida():
    input("Presione Enter para continuar...")


def tryPin(passwordBinFile):
    pin = getpass.getpass(prompt="Ingresa el PIN: ")
    decryptedPassword = Crypto.decryptPassword(
        passwordBinFile, pin)

    if decryptedPassword:
        clearCli()
        print("Pin correcto")
        pausa(2)
        return decryptedPassword


def verifyPin():
    while True:
        pin1 = getpass.getpass(prompt="Ingresa el PIN: ")
        pin2 = getpass.getpass(prompt="Confirme el PIN: ")
        if pin1 == pin2:
            clearCli()
            print('\nLos pines ingresados coinciden\n')
            pausa(1)
            return pin1
        else:
            clearCli()
            print('\nPines distintos, intenta nuevamente.\n')
            pausa(1)
            clearCli()


def copyToClipboard(password, tiempoEspera):
    autoCopy = Settings.autoCopyPassword
    clearCli()
    if not autoCopy:
        opcion = input("¿Desea copiar la contraseña al portapapeles? [S/N] ")
    if autoCopy or opcion in ["S", "s"]:
        pyperclip.copy("")
        pyperclip.copy(password)
        print(f"Contraseña copiada al portapapeles. Se borrará en {
              tiempoEspera}s")
        pausa(tiempoEspera)
        pyperclip.copy("")
        return True
    print(f"La contraseña es: {password} ")
    print(f"Se borrará en {tiempoEspera}s ")
    pausa(tiempoEspera)
    return False


def recoverPassword(passwordBinFile):
    clearCli()
    tiempoEspera = 5
    file_path = os.path.join(Settings.directory, passwordBinFile)

    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        print(f"El archivo {passwordBinFile} no existe en la ruta {Settings.directory}.")
        pausa(2)
        return False

    print(f"Archivo actual: {passwordBinFile}")

    try:
        with open(file_path, 'rb') as file:
            passwordFile = file.read()
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        pausa(2)
        return False

    decryptedPassword = tryPin(passwordFile)
    if not decryptedPassword:
        clearCli()
        print("PIN incorrecto, verifícalo.")
        pausa(2)
        return False

    if decryptedPassword:
        copyToClipboard(decryptedPassword, tiempoEspera)
        return True


def saveEncryptedPassword(password):
    clearCli()
    opcion = input("¿Desea guardar la contraseña? [S/N] ")
    if opcion in ["S", "s"]:
        pin = verifyPin()
        encryptedPassword = Crypto.encryptPassword(password, pin)
        pathVerificator()
        while True:
            clearCli()
            fileName = input("Ingresa un nombre para el archivo: ")
            filePath = f'{Settings.directory}{fileName}.bin'
            if os.path.exists(filePath):
                print(
                    "Ya existe un archivo con ese nombre. Por favor, elige otro nombre.")
                pausa(2)
            else:
                with open(filePath, 'wb') as file:
                    file.write(encryptedPassword)
                    print("Contraseña cifrada guardada en tus archivos :D.")
                    return True
    return False
