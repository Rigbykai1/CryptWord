from Modules import Utils
import configparser
import os

# Crear archivo de configuración por defecto
def createDefaultConfig():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'autoCopyPassword': 'False',
        'folderName': 'passwords',  # Carpeta predeterminada
        'defaultFile': ''  # Campo para archivo predeterminado
    }
    with open('settings.txt', 'w') as configfile:
        config.write(configfile)
    print("Archivo de configuración creado con valores por defecto.")

# Leer archivo de configuración
config = configparser.ConfigParser()

try:
    if not os.path.exists('settings.txt'):
        createDefaultConfig()
    config.read('settings.txt')

    autoCopyPassword = config.getboolean('SETTINGS', 'autoCopyPassword')
    folderName = config.get('SETTINGS', 'folderName')
    defaultFile = config.get('SETTINGS', 'defaultFile')  # Leer archivo predeterminado
    directory = f"{folderName}/"  # Definir directory

except Exception as e:
    print(f"Ocurrió un error al leer el archivo de configuración: {e}")
    createDefaultConfig()

# Mostrar y seleccionar archivos disponibles en la carpeta
def seleccionar_archivo_predeterminado():
    try:
        archivos = os.listdir(directory)  # Asegúrate de que 'directory' esté disponible
        if not archivos:
            print(f"No se encontraron archivos en la carpeta '{directory}'")
            return None
        print(f"Archivos disponibles en '{directory}':")
        for i, archivo in enumerate(archivos):
            print(f"{i + 1}. {archivo}")

        # Selección del archivo por el usuario
        opcion = input(f"Elija un archivo (1-{len(archivos)}): ")
        if opcion.isdigit() and 1 <= int(opcion) <= len(archivos):
            return archivos[int(opcion) - 1]
        else:
            print("Selección no válida.")
            return None
    except FileNotFoundError:
        print(f"La carpeta '{directory}' no existe.")
        return None

# Menú de opciones
def selectOption():
    print("Ajustes:")
    print("1. Copiar automáticamente la contraseña al portapapeles.")
    print("2. Cambiar ruta de guardado.")
    print("3. Configurar archivo predeterminado.")
    print("4. Salir")
    option = input("Elija una opción: ")
    return option

# Guardar configuración
def saveSettings():
    config.set('SETTINGS', 'autoCopyPassword', str(autoCopyPassword))
    config.set('SETTINGS', 'folderName', folderName)
    config.set('SETTINGS', 'defaultFile', defaultFile)  # Guardar archivo predeterminado
    with open('settings.txt', 'w') as configfile:
        config.write(configfile)

# Manejar activación/desactivación de copiado automático
def handleAutoCopy():
    Utils.clearCli()
    global autoCopyPassword
    autoCopyPassword = not autoCopyPassword
    saveSettings()
    if autoCopyPassword:
        print("Copiado automático de contraseñas activado.")
    else:
        print("Copiado automático de contraseñas desactivado.")
    Utils.pausa(2)

# Manejar cambio de ruta de guardado
def handleNewFolder():
    global folderName, directory
    Utils.clearCli()
    newFolderName = input("Ingrese la nueva ruta de guardado: ")
    if newFolderName:
        folderName = newFolderName
        directory = f"{folderName}/"
        saveSettings()
        print(f"Ruta de guardado cambiada a: {directory}")
        Utils.pausa(2)

# Manejar selección de archivo predeterminado
def handleDefaultFile():
    global defaultFile
    Utils.clearCli()
    if defaultFile:
        print(f"Archivo predeterminado actual: {defaultFile}")
        respuesta = input("¿Desea eliminar el archivo predeterminado? (s/n): ").lower()
        if respuesta == 's':
            defaultFile = ''
            saveSettings()
            print("Archivo predeterminado eliminado.")
        else:
            print("No se realizaron cambios.")
    else:
        nuevo_archivo = seleccionar_archivo_predeterminado()
        if nuevo_archivo:
            defaultFile = nuevo_archivo
            saveSettings()
            print(f"Archivo predeterminado configurado: {defaultFile}")
        else:
            print("No se seleccionó ningún archivo.")
    Utils.pausa(2)

# Función principal que maneja el ciclo del menú
def main():
    global autoCopyPassword, folderName, directory, defaultFile
    while True:
        Utils.clearCli()
        print("------------------------------------------------")
        print(f"Ruta de guardado actual: {directory}")
        print(f"Copiado al portapapeles automático: {autoCopyPassword}")
        if defaultFile:
            print(f"Archivo predeterminado: {defaultFile}")
        else:
            print("No hay archivo predeterminado configurado.")
        print("------------------------------------------------")
        opcion = selectOption()
        if opcion == "1":
            handleAutoCopy()
        elif opcion == "2":
            handleNewFolder()
        elif opcion == "3":
            handleDefaultFile()
        elif opcion == "4":
            print("Cerrando menú...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")
            Utils.pausa(1)

if __name__ == "__main__":
    main()
