import os
from Modules import Settings
import Modules.Utils as Utils

def main():
    Utils.borrarConsola()
    binFile = Utils.seleccionarArchivo(Settings.directorio, "Archivo BIN")

    if binFile:
        Utils.recuperarContrasena(binFile)

if __name__ == "__main__":
    main()
