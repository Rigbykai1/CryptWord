import Modules.PassCopy as PassCopy
import Modules.PassWordEncripter as PassWordEncripter
import Modules.PasswordGen as PasswordGen
import Modules.Utils as Utils
import Modules.Settings as Settings
import time

# Función para mostrar el menú
def mostrar_menu():
    print("1. Cifrar contraseña")
    print("2. Descifrar contraseña")
    print("3. Generar contraseña")
    print("4. Configuración")
    print("5. Salir")

# Función para seleccionar una opción válida del menú
def seleccionar_opcion():
    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")
        if opcion in ["1", "2", "3", "4", "5"]:
            return opcion
        else:
            print("Opción no válida. Intente de nuevo.")
            time.sleep(1)
            Utils.clearCli()

# Función para ejecutar las acciones según la opción elegida
def ejecutar_opcion(opcion):
    if opcion == "1":
        PassWordEncripter.main()
    elif opcion == "2":
        PassCopy.main()
    elif opcion == "3":
        PasswordGen.main()
    elif opcion == "4":
        Settings.main()

# Función para ejecutar el archivo predeterminado
def ejecutar_archivo_predeterminado():
    default_file = Settings.defaultFile
    if default_file:
        print(f"Ejecutando el archivo predeterminado: {default_file}")
        if Utils.recoverPassword(default_file):
            print(f"Contraseña recuperada del archivo: {default_file}")
        else:
            print(f"No se pudo recuperar la contraseña del archivo: {default_file}")
    else:
        print("No hay archivo predeterminado configurado.")

# Función principal que maneja el ciclo del menú
def main():
    Utils.clearCli()
    ejecutar_archivo_predeterminado()  # Ejecuta el archivo predeterminado al inicio
    while True:
        Utils.clearCli()
        opcion = seleccionar_opcion()
        
        if opcion == "5":
            Utils.clearCli()
            print("Saliendo de CryptWord")
            Utils.pausa(2)
            break

        # Ejecutar la opción seleccionada
        ejecutar_opcion(opcion)
        
        # Pausa antes de volver al menú
        time.sleep(1)
        Utils.clearCli()

# Iniciar el programa
if __name__ == "__main__":
    main()
