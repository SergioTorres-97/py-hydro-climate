# Funciones auxiliares para el desarrollo de los códigos
import os
import shutil
from typing import Union


def crear_carpeta(ruta: Union[str, os.PathLike], reescribir: bool = True) -> None:
    '''
    Crea una carpeta en la ruta especificada.

    Si la carpeta ya existe y reescribir=True, elimina la carpeta existente
    y crea una nueva (limpia). Si reescribir=False, simplemente asegura que
    la carpeta exista sin eliminar contenido previo.

    Args:
        ruta: Ruta donde se creará la carpeta
        reescribir: Si True, elimina la carpeta existente antes de crearla.
                    Si False, mantiene el contenido existente (por defecto True)

    Returns:
        None

    Ejemplo:
        >>> crear_carpeta('./resultados')  # Crea o limpia la carpeta
        >>> crear_carpeta('./datos', reescribir=False)  # Solo asegura que exista
    '''
    # Si la carpeta existe y se solicita reescribir, eliminarla completamente
    if os.path.exists(ruta) and reescribir:
        shutil.rmtree(ruta)

    # Crear la carpeta (exist_ok=True evita error si ya existe)
    os.makedirs(ruta, exist_ok=True)