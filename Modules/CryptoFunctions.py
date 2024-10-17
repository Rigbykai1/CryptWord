import os
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


# Función para derivar la clave con PBKDF2
def derivarClave(pin, sal, iteraciones=100000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Longitud adecuada para AES-256
        salt=sal,
        iterations=iteraciones,
        backend=default_backend()
    )
    return kdf.derive(pin.encode())

# Función para generar HMAC
def generarHmac(llave, datos):
    h = hmac.HMAC(llave, hashes.SHA256(), backend=default_backend())
    h.update(datos)
    return h.finalize()

# Función para verificar HMAC
def verificarHmac(llave, datos, mac):
    h = hmac.HMAC(llave, hashes.SHA256(), backend=default_backend())
    h.update(datos)
    h.verify(mac)  # Lanza una excepción si no coincide

# Función para encriptar contraseñas
def encriptarContrasena(contrasena, pin):
    try:
        sal = os.urandom(16)  # Genera una sal aleatoria
        llave = derivarClave(pin, sal)  # Deriva la clave con PBKDF2
        
        iv = os.urandom(16)  # Genera un IV aleatorio para CBC
        cipher = Cipher(algorithms.AES(llave), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Padding de la contraseña para que sea múltiplo del tamaño de bloque
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        contrasenaAlmohadilla = padder.update(contrasena.encode()) + padder.finalize()
        
        # Cifrar la contraseña
        contrasenaCifrada = encryptor.update(contrasenaAlmohadilla) + encryptor.finalize()
        
        # Generar HMAC para asegurar integridad (sal + iv + contrasenaCifrada)
        llaveHmac = derivarClave(pin, sal, iteraciones=200000)  # Usar clave derivada diferente para HMAC
        hmacValor = generarHmac(llaveHmac, sal + iv + contrasenaCifrada)
        
        print("Contraseña encriptada y autenticada")
        return sal + iv + contrasenaCifrada + hmacValor  # Devolver el conjunto de datos: sal + iv + cifrado + hmac
    except Exception as e:
        print(f"Error al encriptar la contraseña: {e}")
        return None

# Función para desencriptar contraseñas
def desencriptarContrasena(datosCifrados, pin):
    try:
        sal = datosCifrados[:16]  # Extraer la sal
        iv = datosCifrados[16:32]  # Extraer el IV
        hmacValor = datosCifrados[-32:]  # Extraer el HMAC (últimos 32 bytes)
        contrasenaCifrada = datosCifrados[32:-32]  # Extraer la contraseña cifrada
        
        # Derivar clave y verificar el HMAC
        llaveHmac = derivarClave(pin, sal, iteraciones=200000)
        verificarHmac(llaveHmac, sal + iv + contrasenaCifrada, hmacValor)
        
        # Derivar la clave para desencriptar
        llave = derivarClave(pin, sal)
        
        # Inicializar el cifrador AES en modo CBC
        cipher = Cipher(algorithms.AES(llave), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Desencriptar la contraseña
        contrasenaAlmohadilla = decryptor.update(contrasenaCifrada) + decryptor.finalize()
        
        # Deshacer el padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        contrasena = unpadder.update(contrasenaAlmohadilla) + unpadder.finalize()
        
        print("Contraseña desencriptada correctamente")
        return contrasena.decode()
    except InvalidSignature:
        print("Error: Los datos han sido alterados o el PIN es incorrecto.")
        return None
    except Exception as e:
        print(f"Error al desencriptar la contraseña: {e}")
        return None
