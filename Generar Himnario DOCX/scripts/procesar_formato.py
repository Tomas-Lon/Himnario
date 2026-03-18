"""
PROCESAR_FORMATO.PY
===================
Aplica formato tipo oración y capitalización consistente a todos los himnos.

Reglas aplicadas:
1. Primera letra de cada oración en mayúscula
2. Nombres divinos siempre capitalizados: Dios, Jesús, Señor, Jesucristo, Cristo, Jehová, Él
3. Detección y conversión de texto en mayúsculas (80%+ threshold)
4. Normalización de CORO/ESTRIBILLO/FINAL con numeración romana

Entrada:
    Himnario_Limpio_Final.txt (cualquier formato)
    
Salida:
    Himnario_Limpio_Final.txt (formateado)
    REPORTE_CAMBIOS.txt

Uso:
    python procesar_formato.py
"""

import re

# Palabras que siempre se capitalizan (nombres divinos)
PALABRAS_ESPECIALES = {
    'dios': 'Dios',
    'jesús': 'Jesús',
    'jesus': 'Jesús',
    'señor': 'Señor',
    'jesucristo': 'Jesucristo',
    'cristo': 'Cristo',
    'jehová': 'Jehová',
    'espíritu': 'Espíritu',
    'santo': 'Santo',
    'él': 'Él'
}

def esta_en_mayusculas(texto):
    """Detecta si el texto está 80% o más en mayúsculas"""
    letras = [c for c in texto if c.isalpha()]
    if len(letras) == 0:
        return False
    mayusculas = sum(1 for c in letras if c.isupper())
    porcentaje = (mayusculas / len(letras)) * 100
    return porcentaje >= 80

def capitalizar_palabra_especial(palabra, es_primera=False):
    """Capitaliza palabras divinas manteniendo puntuación"""
    palabra_limpia = palabra.lower().strip('.,;:!?¡¿()[]{}"\'')
    
    if palabra_limpia in PALABRAS_ESPECIALES:
        nueva = PALABRAS_ESPECIALES[palabra_limpia]
        # Reconstruir con puntuación original
        for i, c in enumerate(palabra):
            if not c.isalpha():
                nueva = palabra[:i] + nueva + palabra[i+len(palabra_limpia):]
                break
        return nueva
    
    return palabra

def capitalizar_oracion(texto):
    """Aplica formato tipo oración con capitalización de nombres divinos"""
    # Dividir en oraciones por puntuación
    oraciones = re.split(r'([.!?;]\s+)', texto)
    
    resultado = []
    for i, parte in enumerate(oraciones):
        if i % 2 == 0:  # Texto (no separador)
            if parte.strip():
                # Primera letra en mayúscula
                parte = parte[0].upper() + parte[1:].lower() if len(parte) > 0 else parte
                
                # Capitalizar palabras especiales
                palabras = parte.split()
                palabras_corregidas = []
                for j, palabra in enumerate(palabras):
                    palabra_corregida = capitalizar_palabra_especial(palabra, j == 0)
                    palabras_corregidas.append(palabra_corregida)
                
                parte = ' '.join(palabras_corregidas)
                resultado.append(parte)
        else:  # Separador
            resultado.append(parte)
    
    return ''.join(resultado)

def es_marcador_coro(linea):
    """Detecta CORO, ESTRIBILLO, FINAL con numeración romana opcional"""
    return bool(re.match(r'^\s*(CORO|ESTRIBILLO|FINAL)(\s+[IVX]+)?:?\s*$', linea.strip(), re.IGNORECASE))

def normalizar_marcador_coro(linea):
    """Normaliza formato de CORO/ESTRIBILLO/FINAL"""
    match = re.match(r'^\s*(CORO|ESTRIBILLO|FINAL)(\s+[IVX]+)?\s*:?\s*$', linea.strip(), re.IGNORECASE)
    if match:
        palabra = match.group(1).upper()
        numero = match.group(2).upper() if match.group(2) else ''
        return f"{palabra}{numero}:"
    return linea

def procesar_linea(linea):
    """Procesa una línea individual"""
    if not linea.strip():
        return linea
    
    # No procesar marcadores de CORO
    if es_marcador_coro(linea):
        return normalizar_marcador_coro(linea)
    
    # Convertir si está en mayúsculas
    if esta_en_mayusculas(linea):
        linea = linea.lower()
    
    # Aplicar formato de oración
    return capitalizar_oracion(linea)

def procesar_titulo(titulo):
    """Procesa el título capitalizando palabras importantes"""
    palabras = titulo.split()
    resultado = []
    
    for palabra in palabras:
        palabra_limpia = palabra.lower().strip('.,;:!?¡¿()[]{}"\'')
        if palabra_limpia in PALABRAS_ESPECIALES:
            palabra_corregida = capitalizar_palabra_especial(palabra)
            resultado.append(palabra_corregida)
        else:
            # Primera letra en mayúscula
            resultado.append(palabra[0].upper() + palabra[1:] if len(palabra) > 0 else palabra)
    
    return ' '.join(resultado)

def procesar_himno(numero, titulo, letra):
    """Procesa un himno completo"""
    # Procesar título
    titulo_procesado = procesar_titulo(titulo)
    
    # Procesar letra línea por línea
    lineas = letra.split('\n')
    lineas_procesadas = [procesar_linea(linea) for linea in lineas]
    letra_procesada = '\n'.join(lineas_procesadas)
    
    return titulo_procesado, letra_procesada

def main():
    """Función principal"""
    print('=' * 80)
    print('PROCESADOR DE FORMATO Y CAPITALIZACIÓN')
    print('=' * 80)
    
    # Leer archivo
    import os
    post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
    archivo_entrada = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
    archivo_salida = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
    archivo_reporte = os.path.join(post_dir, 'REPORTE_CAMBIOS.txt')
    print('\n[1/3] Leyendo Himnario_Limpio_Final.txt de post-proceso/...')
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            contenido = f.read()
    print('[2/3] Procesando formato...')
    patron = r'(\d+)\.\s+(.+?)\n((?:(?!\n\d+\.\s).)+)'
    himnos = re.findall(patron, contenido, re.DOTALL)
    print(f'      Total de himnos: {len(himnos)}')
    
    # Procesar cada himno
    himnos_procesados = []
    cambios_detectados = []
    
    for numero, titulo, letra in himnos:
        titulo_proc, letra_proc = procesar_himno(numero, titulo.strip(), letra)
        
        # Detectar si hubo cambios
        if titulo.strip() != titulo_proc or letra != letra_proc:
            cambios_detectados.append({
                'numero': numero,
                'titulo_orig': titulo.strip(),
                'titulo_nuevo': titulo_proc
            })
        
        himnos_procesados.append((numero, titulo_proc, letra_proc))
    
    print(f'      Himnos modificados: {len(cambios_detectados)}')
    
    # Guardar archivo procesado
    print('[3/3] Guardando archivos...')
    print('[3/3] Guardando archivos en post-proceso/...')
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for numero, titulo, letra in himnos_procesados:
            f.write(f"{numero}. {titulo}\n")
            f.write(f"{letra}\n\n")
    # Guardar reporte de cambios
    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        f.write('=' * 80 + '\n')
        f.write('REPORTE DE PROCESAMIENTO DE FORMATO\n')
        f.write('=' * 80 + '\n\n')
        f.write(f'Total de himnos procesados: {len(himnos)}\n')
        f.write(f'Himnos con cambios: {len(cambios_detectados)}\n\n')
        if cambios_detectados:
            f.write('=' * 80 + '\n')
            f.write('DETALLE DE CAMBIOS\n')
            f.write('=' * 80 + '\n\n')
            for cambio in cambios_detectados:
                f.write(f"Himno #{cambio['numero']}\n")
                if cambio['titulo_orig'] != cambio['titulo_nuevo']:
                    f.write(f"  Título original: {cambio['titulo_orig']}\n")
                    f.write(f"  Título nuevo: {cambio['titulo_nuevo']}\n")
                f.write('\n')
    # Guardar reporte de cambios
    with open('REPORTE_CAMBIOS.txt', 'w', encoding='utf-8') as f:
        f.write('=' * 80 + '\n')
        f.write('REPORTE DE PROCESAMIENTO DE FORMATO\n')
        f.write('=' * 80 + '\n\n')
        f.write(f'Total de himnos procesados: {len(himnos)}\n')
        f.write(f'Himnos con cambios: {len(cambios_detectados)}\n\n')
        
        if cambios_detectados:
            f.write('=' * 80 + '\n')
            f.write('DETALLE DE CAMBIOS\n')
            f.write('=' * 80 + '\n\n')
            for cambio in cambios_detectados:
                f.write(f"Himno #{cambio['numero']}\n")
                if cambio['titulo_orig'] != cambio['titulo_nuevo']:
                    f.write(f"  Título original: {cambio['titulo_orig']}\n")
                    f.write(f"  Título nuevo: {cambio['titulo_nuevo']}\n")
                f.write('\n')
    
    print('\n' + '=' * 80)
        print('OK Archivos actualizados:')
    print('  - Himnario_Limpio_Final.txt (formateado)')
    print('  - REPORTE_CAMBIOS.txt')
    print(f'\n✓ Cambios aplicados a {len(cambios_detectados)} himnos')
    print('=' * 80)

if __name__ == '__main__':
    main()
