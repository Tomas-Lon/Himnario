"""
EXTRAER_DESDE_RTF.PY
====================
Extrae el texto limpio de un archivo RTF y lo guarda como TXT para el pipeline.

Uso:
    python extraer_desde_rtf.py

Dependencia:
    pip install striprtf
"""

import os
import re
from striprtf.striprtf import rtf_to_text

# Configuración de rutas
pre_dir = os.path.join(os.path.dirname(__file__), '..', 'pre-proceso')
post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
archivo_rtf = os.path.join(pre_dir, 'Himario_TabernaculoLaEsperanza_V2.docx.rtf')
archivo_txt = os.path.join(pre_dir, 'Himario_TabernaculoLaEsperanza_V2.docx.txt')

print('='*80)
print('EXTRACTOR DE TEXTO DESDE RTF')
print('='*80)

# Leer y extraer texto
with open(archivo_rtf, 'r', encoding='utf-8') as f:
    rtf_content = f.read()
texto = rtf_to_text(rtf_content)

# Guardar como TXT

# Postprocesar para agregar separadores
def agregar_separadores(texto):
    lineas = texto.split('\n')
    resultado = []
    patron_coro = re.compile(r'^\s*(coro|estribillo|final)(\s+[ivx]+)?\s*:?', re.IGNORECASE)
    for linea in lineas:
        resultado.append(linea)
        # Agregar línea vacía después de marcador de coro o estrofa (línea vacía después de punto final)
        if patron_coro.match(linea) or (linea.strip().endswith('.') and len(linea.strip()) > 3):
            resultado.append('')
    return '\n'.join(resultado)

texto_separado = agregar_separadores(texto)
with open(archivo_txt, 'w', encoding='utf-8') as f:
    f.write(texto_separado)

print(f'OK Texto extraído y guardado en: {archivo_txt} (con separadores)')
print('='*80)
