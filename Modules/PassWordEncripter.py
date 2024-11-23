import Modules.Utils as Utils


def main():
    password = input("Ingresa la contraseña a cifrar: ")
    try:
        Utils.guardarArchivoBin(password)
    except Exception as e:
        print(f"Oops, parece que hubo un error: {e}")

if __name__ == "__main__":
    main()