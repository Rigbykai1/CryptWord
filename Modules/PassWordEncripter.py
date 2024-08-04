import os
import Modules.Utils as Utils
import Modules.CryptoFunctions as Crypto

def savePassword(password, pin):
    encryptedPassword = Crypto.encryptPassword(password, pin)
    if not os.path.exists('Passwords'):
        os.makedirs('Passwords')
    
    while True:
        fileName = input("Ingresa un nombre para el archivo: ")
        filePath = f'Passwords/{fileName}.bin'
        if os.path.exists(filePath):
            print("Ya existe un archivo con ese nombre. Por favor, elige otro nombre.")
        else:
            with open(filePath, 'wb') as file:
                file.write(encryptedPassword)
                print("Contraseña cifrada guardada en tus archivos :D.")
            break
        
def main():
    password = input("Ingresa la contraseña a cifrar: ")
    pin = Utils.verifyPin()
    try:
        savePassword(password, pin)
    except Exception as e:
        print(f"Oops, parece que hubo un error: {e}")

if __name__ == "__main__":
    main()
