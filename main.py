import Modules.PassCopy as PassCopy
import Modules.PassWordEncripter as PassWordEncripter
import Modules.PasswordGen as PasswordGen
import Modules.Utils as Utils
import Modules.Settings as Settings

# Función para mostrar el menú
def mostrarMenu():
    print("1. Cifrar contraseña")
    print("2. Descifrar contraseña")
    print("3. Generar contraseña")
    print("4. Configuración")
    print("5. Salir")

# Función para seleccionar una opción válida del menú
def seleccionarOpcion():
    while True:
        mostrarMenu()
        opcion = input("Elija una opción: ")
        if opcion in ["1", "2", "3", "4", "5"]:
            return opcion
        else:
            print("Opción no válida. Intente de nuevo.")
            Utils.pausa(1)
            Utils.borrarConsola()

# Función para ejecutar las acciones según la opción elegida
def ejecutarOpcion(opcion):
    if opcion == "1":
        PassWordEncripter.main()
    elif opcion == "2":
        PassCopy.main()
    elif opcion == "3":
        PasswordGen.main()
    elif opcion == "4":
        Settings.main()

# Función para ejecutar el archivo predeterminado
def ejecutarArchivoPredeterminado():
    archivoPredeterminado = Settings.archivoPorDefecto
    if archivoPredeterminado:
        if Utils.recuperarContrasena(archivoPredeterminado):
            Utils.borrarConsola()
            print(f"Contraseña recuperada del exitosamente.")
    else:
        Utils.borrarConsola()
        print("No hay archivo predeterminado configurado.")
    Utils.pausa(2)

# Función principal que maneja el ciclo del menú
def main():
    Utils.borrarConsola()
    ejecutarArchivoPredeterminado()
    while True:
        Utils.borrarConsola()
        opcion = seleccionarOpcion()
        
        if opcion == "5":
            Utils.borrarConsola()
            print("Saliendo de CryptWord")
            Utils.pausa(2)
            break

        ejecutarOpcion(opcion)
        
        Utils.pausa(1)

# Iniciar el programa
if __name__ == "__main__":
    main()
