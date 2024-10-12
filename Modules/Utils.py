import os
import time
import getpass
import pyperclip
import Modules.CryptoFunctions as Crypto
from Modules import Settings


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


def ingresarPin(archivoContrasenaBin, nombreArchivo):
    while True:
        borrarConsola()
        print(f"Archivo actual {nombreArchivo}")
        print("Escriba el PIN o use como contraseña 'salir' para cancelar.")
        pin = getpass.getpass(prompt="Ingresa el PIN: ")

        if pin == 'salir':
            despedida = print("Saliendo...")
            pausa(2)
            return despedida
        decryptedPassword = Crypto.desencriptarContrasena(archivoContrasenaBin, pin)

        if decryptedPassword:
            borrarConsola()
            print("PIN correcto")
            pausa(2)
            return decryptedPassword
        else:
            print("PIN incorrecto, verifica tu entrada.")
        pausa(2)


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


def copiarEnPortapapeles(contrasena, tiempoEspera):
    autoCopy = Settings.autoCopiarContrasena
    borrarConsola()
    if not autoCopy:
        opcion = input("¿Desea copiar la contraseña al portapapeles? [S/N] ")
    if autoCopy or opcion in ["S", "s"]:
        pyperclip.copy("")
        pyperclip.copy(contrasena)
        print(f"Contraseña copiada al portapapeles. Se borrará en {
              tiempoEspera}s")
        pausa(tiempoEspera)
        pyperclip.copy("")
        return True
    print(f"La contraseña es: {contrasena} ")
    print(f"Se borrará en {tiempoEspera}s ")
    pausa(tiempoEspera)
    return False


def recuperarContrasena(nombreArchivo):
    borrarConsola()
    tiempoEspera = 5
    directorio = os.path.join(Settings.directorio, nombreArchivo)

    if not os.path.exists(directorio):
        print(f"El archivo {nombreArchivo} no existe en la ruta {Settings.directorio}.")
        pausa(2)
        return False

    print(f"Archivo actual: {nombreArchivo}")
    try:
        with open(directorio, 'rb') as file:
            archivoBin = file.read()
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        pausa(2)
        return False
    
    desencriptarContrasena = ingresarPin(archivoBin, nombreArchivo)
    
    if desencriptarContrasena:
        copiarEnPortapapeles(desencriptarContrasena, tiempoEspera)
        return True

def guardarArchivoBin(contrasena):
    borrarConsola()
    opcion = input("¿Desea guardar la contraseña? [S/N] ")
    if opcion in ["S", "s"]:
        pin = verificarPin()
        contrasenaEncriptada = Crypto.encriptarContrasena(contrasena, pin)
        if not os.path.exists(Settings.nombreFolder):
            os.makedirs(Settings.nombreFolder)
        while True:
            borrarConsola()
            nombreArchivo = input("Ingresa un nombre para el archivo: ")
            directorio = f'{Settings.directorio}{nombreArchivo}.bin'
            if os.path.exists(directorio):
                print(
                    "Ya existe un archivo con ese nombre. Por favor, elige otro nombre.")
                pausa(2)
            else:
                with open(directorio, 'wb') as file:
                    file.write(contrasenaEncriptada)
                    print("Contraseña cifrada guardada en tus archivos :D.")
                    return True
    return False
