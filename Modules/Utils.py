import os
import time
import getpass
import pyperclip
import Modules.CryptoFunctions as Crypto
from Modules import Settings


def verificadorDeRuta():
    if not os.path.exists(Settings.nombreFolder):
        os.makedirs(Settings.nombreFolder)

def leerArchivos(directorio):
    archivos = os.listdir(directorio)
    if not archivos:
        print("No hay contraseñas guardadas.")
        return []
    return archivos

def seleccionarArchivo(directorio, mensaje):
    try:
        archivos = leerArchivos(directorio)
        if not archivos:
            print(f"No se encontraron archivos en la carpeta '{directorio}'")
            return None
        
        # Mostrar archivos disponibles
        print(mensaje)
        for i, archivo in enumerate(archivos):
            print(f"{i + 1}. {archivo}")

        # Solicitar selección de archivo
        opcion = input(f"Elija un archivo (1-{len(archivos)}): ")
        if opcion.isdigit() and 1 <= int(opcion) <= len(archivos):
            return archivos[int(opcion) - 1]
        else:
            print("Selección no válida.")
            return None
    except FileNotFoundError:
        print(f"La carpeta '{directorio}' no existe.")
        return None
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None

def borrarConsola():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa(timer):
    time.sleep(timer)


def pausaInterrumpida():
    input("Presione Enter para continuar...")


def ingresarPin(passwordBinFile):
    pin = getpass.getpass(prompt="Ingresa el PIN: ")
    decryptedPassword = Crypto.desencriptarContrasena(
        passwordBinFile, pin)

    if decryptedPassword:
        borrarConsola()
        print("Pin correcto")
        pausa(2)
        return decryptedPassword


def verificarPin():
    while True:
        pin1 = getpass.getpass(prompt="Ingresa el PIN: ")
        pin2 = getpass.getpass(prompt="Confirme el PIN: ")
        if pin1 == pin2:
            borrarConsola()
            print('\nLos pines ingresados coinciden\n')
            pausa(1)
            return pin1
        else:
            borrarConsola()
            print('\nPines distintos, intenta nuevamente.\n')
            pausa(1)
            borrarConsola()


def copiarEnPortapapeles(password, tiempoEspera):
    autoCopy = Settings.autoCopiarContrasena
    borrarConsola()
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


def recuperarContrasena(archivoBin):
    borrarConsola()
    tiempoEspera = 5
    directorio = os.path.join(Settings.directorio, archivoBin)

    if not os.path.exists(directorio):
        print(f"El archivo {archivoBin} no existe en la ruta {Settings.directorio}.")
        pausa(2)
        return False

    print(f"Archivo actual: {archivoBin}")

    try:
        with open(directorio, 'rb') as file:
            archivoContrasena = file.read()
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        pausa(2)
        return False

    desencriptarContrasena = ingresarPin(archivoContrasena)
    if not desencriptarContrasena:
        borrarConsola()
        print("PIN incorrecto, verifícalo.")
        pausa(2)
        return False

    if desencriptarContrasena:
        copiarEnPortapapeles(desencriptarContrasena, tiempoEspera)
        return True


def saveEncryptedPassword(password):
    borrarConsola()
    opcion = input("¿Desea guardar la contraseña? [S/N] ")
    if opcion in ["S", "s"]:
        pin = verificarPin()
        encryptedPassword = Crypto.encriptarContrasena(password, pin)
        verificadorDeRuta()
        while True:
            borrarConsola()
            fileName = input("Ingresa un nombre para el archivo: ")
            filePath = f'{Settings.directorio}{fileName}.bin'
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
