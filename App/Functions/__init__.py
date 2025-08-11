# App/Functions/__init__.py
"""
Paquete de funciones principales para el procesamiento y envío de datos.
Aquí centralizamos las importaciones más utilizadas para facilitar el uso
en el resto del proyecto.
"""

from .reader import leer_solo_tabla_csv_filtrado, REQUIRED_COLS, file_fingerprint
from .payloads import build_json_para_n8n
from .sender import send

