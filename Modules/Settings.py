from Modules import Utils
import configparser
import os

# Crear archivo de configuración por defecto
def crearArchivoPorDefecto():
    configuracion = configparser.ConfigParser()
    configuracion['SETTINGS'] = {
        'autoCopiarContrasena': 'False', # Desactivado por defecto
        'nombreFolder': 'passwords',  # Carpeta predeterminada "/passwords"
        'archivoPorDefecto': ''  # Campo para archivo predeterminado "settings.txt"
    }
    with open('settings.txt', 'w') as archivoDeConfiguracion:
        configuracion.write(archivoDeConfiguracion)
    print("Archivo de configuración creado con valores por defecto.")

# Leer archivo de configuración
configuracion = configparser.ConfigParser()

try:
    if not os.path.exists('settings.txt'):
        crearArchivoPorDefecto()
    configuracion.read('settings.txt')

    autoCopiarContrasena = configuracion.getboolean('SETTINGS', 'autoCopiarContrasena')
    nombreFolder = configuracion.get('SETTINGS', 'nombreFolder')
    archivoPorDefecto = configuracion.get('SETTINGS', 'archivoPorDefecto')  # Leer archivo predeterminado
    directorio = f"{nombreFolder}/"  # Definir directorio

except Exception as e:
    print(f"Ocurrió un error al leer el archivo de configuración: {e}")
    crearArchivoPorDefecto()


# Menú de opciones
def seleccionarOpcion():
    print("Ajustes:")
    print("1. Copiar automáticamente la contraseña al portapapeles.")
    print("2. Cambiar ruta de guardado.")
    print("3. Configurar archivo predeterminado.")
    print("4. Salir")
    option = input("Elija una opción: ")
    return option

# Guardar configuración
def guardarConfiguracion():
    configuracion.set('SETTINGS', 'autoCopiarContrasena', str(autoCopiarContrasena))
    configuracion.set('SETTINGS', 'nombreFolder', nombreFolder)
    configuracion.set('SETTINGS', 'archivoPorDefecto', archivoPorDefecto)  # Guardar archivo predeterminado
    with open('settings.txt', 'w') as archivoDeConfiguracion:
        configuracion.write(archivoDeConfiguracion)

# Manejar activación/desactivación de copiado automático
def cambiarAutoCopiado():
    Utils.borrarConsola()
    global autoCopiarContrasena
    autoCopiarContrasena = not autoCopiarContrasena
    guardarConfiguracion()
    if autoCopiarContrasena:
        print("Copiado automático de contraseñas activado.")
    else:
        print("Copiado automático de contraseñas desactivado.")
    Utils.pausa(2)

# Manejar cambio de ruta de guardado
def handleNewFolder():
    global nombreFolder, directorio
    Utils.borrarConsola()
    folderNuevo = input("Ingrese la nueva ruta de guardado: ")
    if folderNuevo:
        nombreFolder = folderNuevo
        directorio = f"{nombreFolder}/"
        guardarConfiguracion()
        print(f"Ruta de guardado cambiada a: {directorio}")
        Utils.pausa(2)

# Manejar selección de archivo predeterminado
def cambiarArchivoPorDefecto():
    global archivoPorDefecto
    Utils.borrarConsola()
    if archivoPorDefecto:
        print(f"Archivo predeterminado actual: {archivoPorDefecto}")
        respuesta = input("¿Desea eliminar el archivo predeterminado? (s/n): ").lower()
        if respuesta == 's':
            archivoPorDefecto = ''
            guardarConfiguracion()
            print("Archivo predeterminado eliminado.")
        else:
            print("No se realizaron cambios.")
    else:
        archivoNuevo = Utils.seleccionarArchivo(directorio, "Archivo por defecto")
        if archivoNuevo:
            archivoPorDefecto = archivoNuevo
            guardarConfiguracion()
            print(f"Archivo predeterminado configurado: {archivoPorDefecto}")
        else:
            print("No se seleccionó ningún archivo.")
    Utils.pausa(2)

# Función principal que maneja el ciclo del menú
def main():
    global autoCopiarContrasena, nombreFolder, directorio, archivoPorDefecto
    while True:
        Utils.borrarConsola()
        print("------------------------------------------------")
        print(f"Ruta de guardado actual: {directorio}")
        print(f"Copiado al portapapeles automático: {autoCopiarContrasena}")
        if archivoPorDefecto:
            print(f"Archivo predeterminado: {archivoPorDefecto}")
        else:
            print("No hay archivo predeterminado configurado.")
        print("------------------------------------------------")
        opcion = seleccionarOpcion()
        if opcion == "1":
            cambiarAutoCopiado()
        elif opcion == "2":
            handleNewFolder()
        elif opcion == "3":
            cambiarArchivoPorDefecto()
        elif opcion == "4":
            print("Cerrando menú...")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")
            Utils.pausa(1)

if __name__ == "__main__":
    main()
