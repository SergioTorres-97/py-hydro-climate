#Funciones auxiliares para el desarrollo de los códigos
import os
import shutil

def crear_carpeta(ruta, reescribir=True):
    if os.path.exists(ruta) and reescribir:
        shutil.rmtree(ruta)

    os.makedirs(ruta, exist_ok=True)