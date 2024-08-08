from Modules import Utils
import configparser
import os


def createDefaultConfig():
    config = configparser.ConfigParser()
    config['SETTINGS'] = {
        'autoCopyPassword': 'False',
        'folderName': 'passwords'
    }
    with open('settings.txt', 'w') as configfile:
        config.write(configfile)
    print("Archivo de configuración creado con valores por defecto.")


config = configparser.ConfigParser()

try:
    if not os.path.exists('settings.txt'):
        createDefaultConfig()
    config.read('settings.txt')

    autoCopyPassword = config.getboolean('SETTINGS', 'autoCopyPassword')
    folderName = config.get('SETTINGS', 'folderName')
    directory = f"{folderName}/"

except Exception as e:
    print(f"Ocurrió un error al leer el archivo de configuración: {e}")
    createDefaultConfig()


def selectOption():
    print("Ajustes:")
    print("1. Copiar automáticamente la contraseña al portapapeles.")
    print("2. Cambiar ruta de guardado.")
    print("3. Salir")
    option = int(input("Elija una opción: "))
    return option


def saveSettings():
    config.set('SETTINGS', 'autoCopyPassword', str(autoCopyPassword))
    config.set('SETTINGS', 'folderName', folderName)
    with open('settings.txt', 'w') as configfile:
        config.write(configfile)


def handleAutoCopy():
    Utils.clearCli()
    global autoCopyPassword
    autoCopyPassword = not autoCopyPassword
    saveSettings()
    if autoCopyPassword:
        print("Copiado automático de contraseñas activada.")
    else:
        print("Copiado automático de contraseñas desactivada.")
    Utils.pausa(2)


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


def main():
    global autoCopyPassword, folderName, directory
    while True:
        Utils.clearCli()
        print("------------------------------------------------")
        print(f"Ruta de guardado actual: {directory}")
        print(f"Copiado al portapapeles automático: {autoCopyPassword}")
        print("------------------------------------------------")
        opcion = selectOption()
        if opcion == 1:
            handleAutoCopy()
        elif opcion == 2:
            handleNewFolder()
        elif opcion == 3:
            print("Cerrando menu...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")


if __name__ == "__main__":
    main()
