import string
import random as rand
import Modules.Utils as Utils
import Modules.PassWordEncripter as PassWordEncripter
import pyperclip

def randomNumber(limite):
    numeroRandom = rand.randint(0, limite)
    return numeroRandom

def genPassword(limite):
    letras = list(string.ascii_letters)
    numeros = list(string.digits)
    caracteres = list(string.punctuation)
    password = []
    
    for i in range(limite):
        limiter = randomNumber(100)
        rand.shuffle(letras)
        rand.shuffle(numeros)
        rand.shuffle(caracteres)
        if limiter < 30:
            character = rand.choice(letras)
        elif limiter < 60:
            character = rand.choice(numeros)
        else:
            character = rand.choice(caracteres)
        password.append(character)

    rand.shuffle(password)
    return ''.join(password)

def savePasswordBin(password):
    pin = Utils.verifyPin()
    PassWordEncripter.savePassword(password, pin)

def main():
    try:
        limit = int(input("Ingresa en tamaño de la contraseña: "))
        password = genPassword(limit)
        print(f'Contraseña creada: {password}')
        pyperclip.copy("")
        pyperclip.copy(password)
        print('Contraseña copiada en el portapapeles')            
    except:
        print('Debes ingresar un numero.')
        main()
        
    opcion = input('Desea guardar la contraseña [S/N]: ')
    if opcion.upper() == "S":
        savePasswordBin(password)
        print("Contraseña guardada")
        Utils.pausa(2)
    
if __name__ == "__main__":
    main()
