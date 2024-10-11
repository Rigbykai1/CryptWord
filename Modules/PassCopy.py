import os
from Modules import Settings
import Modules.Utils as Utils

def main():
    Utils.borrarConsola()
    binFile = Utils.seleccionarArchivo(Settings.directorio, "Archivo BIN")
    if not binFile:
        Utils.pausa(2)
    else:
        while True:
            Utils.borrarConsola()
            if Utils.recuperarContrasena(binFile):
                break

if __name__ == "__main__":
    main()
