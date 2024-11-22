import string
import random as rand
import Modules.Utils as Utils
import Modules.PassWordEncripter as PassWordEncripter


def generadorDeContrasenas(limite):
    porcentajeLetras = 30
    porcentajeNumeros = 30
    porcentajeCaracteres = 40
    if porcentajeLetras + porcentajeNumeros + porcentajeCaracteres != 100:
        raise ValueError("Los porcentajes deben sumar 100.")

    letras = list(string.ascii_letters)
    numeros = list(string.digits)
    caracteres = list(string.punctuation)
    contrasena = []

    # Calcular la cantidad de caracteres de cada tipo
    cantidadLetras = (porcentajeLetras * limite) // 100
    cantidadNumeros = (porcentajeNumeros * limite) // 100
    cantidadCaracteres = limite - cantidadLetras - cantidadNumeros

    # Añadir caracteres de cada tipo
    contrasena.extend(rand.choices(letras, k=cantidadLetras))
    contrasena.extend(rand.choices(numeros, k=cantidadNumeros))
    contrasena.extend(rand.choices(caracteres, k=cantidadCaracteres))

    # Mezclar los caracteres para asegurar la aleatoriedad
    rand.shuffle(contrasena)
    return ''.join(contrasena)


def main():
    Utils.borrarConsola()
    try:
        limit = int(input("Ingresa en tamaño de la contraseña: "))
        if limit < 8:
            raise ValueError(
                "La longitud de la contraseña debe ser al menos 8 caracteres.")
        password = generadorDeContrasenas(limit)
        print(f'Contraseña creada: {password}')
        Utils.copiarEnPortapapeles(password, 5)
        Utils.guardarArchivoBin(password)
    except ValueError as ve:
        print(f'Error: {ve}')
        Utils.pausa(1)
        main()
    except Exception as e:
        print(f'Ocurrió un error: {e}')
        Utils.pausa(1)
        main()


if __name__ == "__main__":
    main()
