"""
PARSEAR_TXT_WORD.PY
===================
Extrae himnos desde un archivo TXT exportado de Word y los convierte
al formato estándar del himnario.

Detecta:
- Índice de himnos
- Contenido de cada himno
- Inconsistencias entre índice y contenido

Uso:
    1. Exporta el documento Word a formato "Texto sin formato (.txt)"
    2. Coloca el archivo en esta carpeta
    3. Ejecuta: python parsear_txt_word.py

Salida:
    Himnario_Extraido.txt
"""

import re

def extraer_indice(contenido):
    """Extrae el índice de himnos del inicio del documento"""
    # Buscar líneas con formato: "número. Título"
    patron_indice = r'^(\d+)\.\s+(.+)$'
    lineas = contenido.split('\n')
    
    indice = {}
    for linea in lineas[:500]:  # Buscar en las primeras 500 líneas
        match = re.match(patron_indice, linea.strip())
        if match:
            num = int(match.group(1))
            titulo = match.group(2).strip()
            indice[num] = titulo
    
    return indice

def extraer_himnos(contenido):
    """Extrae el contenido completo de cada himno"""
    # Patrón: número. Título seguido de contenido hasta el próximo número
    patron = r'(\d+)\.\s+(.+?)\n((?:(?!\n\d+\.\s).)+)'
    matches = re.findall(patron, contenido, re.DOTALL)
    
    himnos = {}
    for num_str, titulo, letra in matches:
        num = int(num_str)
        himnos[num] = {
            'titulo': titulo.strip(),
            'letra': letra.strip()
        }
    
    return himnos

def detectar_inconsistencias(indice, himnos):
    """Detecta diferencias entre el índice y el contenido"""
    inconsistencias = []
    
    # Himnos en índice sin contenido
    sin_contenido = set(indice.keys()) - set(himnos.keys())
    if sin_contenido:
        inconsistencias.append(f"Himnos en índice sin contenido: {len(sin_contenido)}")
        for num in sorted(sin_contenido):
            inconsistencias.append(f"  #{num}: {indice[num]}")
    
    # Himnos con contenido sin índice
    sin_indice = set(himnos.keys()) - set(indice.keys())
    if sin_indice:
        inconsistencias.append(f"\nHimnos con contenido sin índice: {len(sin_indice)}")
        for num in sorted(sin_indice):
            inconsistencias.append(f"  #{num}: {himnos[num]['titulo']}")
    
    # Títulos diferentes
    titulos_diferentes = []
    for num in set(indice.keys()) & set(himnos.keys()):
        if indice[num].lower() != himnos[num]['titulo'].lower():
            titulos_diferentes.append((num, indice[num], himnos[num]['titulo']))
    
    if titulos_diferentes:
        inconsistencias.append(f"\nTítulos diferentes: {len(titulos_diferentes)}")
        for num, titulo_indice, titulo_contenido in titulos_diferentes:
            inconsistencias.append(f"  #{num}:")
            inconsistencias.append(f"    Índice: {titulo_indice}")
            inconsistencias.append(f"    Contenido: {titulo_contenido}")
    
    return inconsistencias

def main():
    """Función principal"""
    print('=' * 80)
    print('EXTRACTOR DE HIMNOS DESDE WORD TXT')
    print('=' * 80)
    
    # Selección automática o por argumento
    import os
    import sys
    pre_dir = os.path.join(os.path.dirname(__file__), '..', 'pre-proceso')
    post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
    archivos_txt = [f for f in os.listdir(pre_dir) if f.endswith('.txt')]
    if not archivos_txt:
        print('⚠ No se encontraron archivos .txt en pre-proceso/')
        return
    if len(sys.argv) > 1:
        archivo_input = sys.argv[1]
        if archivo_input not in archivos_txt:
            print(f'⚠ El archivo {archivo_input} no se encuentra en pre-proceso/')
            return
    else:
        archivo_input = archivos_txt[0]
        print(f'✓ Seleccionado automáticamente: {archivo_input}')
    archivo_path = os.path.join(pre_dir, archivo_input)
    print(f'\n[1/4] Leyendo {archivo_input}...')
    with open(archivo_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Extraer índice
    print('[2/4] Extrayendo índice...')
    indice = extraer_indice(contenido)
    print(f'      Himnos en índice: {len(indice)}')
    
    # Extraer contenido
    print('[3/4] Extrayendo contenido de himnos...')
    himnos = extraer_himnos(contenido)
    print(f'      Himnos con contenido: {len(himnos)}')
    
    # Detectar inconsistencias
    print('[4/4] Detectando inconsistencias...')
    inconsistencias = detectar_inconsistencias(indice, himnos)
    
    if inconsistencias:
        print('\n⚠ INCONSISTENCIAS ENCONTRADAS:')
        for inc in inconsistencias:
            print(inc)
    else:
        print('      ✓ No se encontraron inconsistencias')
    
    # Guardar archivo extraído y copia para el pipeline
    archivo_salida1 = os.path.join(post_dir, 'Himnario_Extraido.txt')
    archivo_salida2 = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
    for archivo_salida in [archivo_salida1, archivo_salida2]:
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            for num in sorted(himnos.keys()):
                f.write(f"{num}. {himnos[num]['titulo']}\n")
                f.write(f"{himnos[num]['letra']}\n\n")
    print('\n' + '=' * 80)
    print(f'✓ Archivos generados:')
    print(f'   - {archivo_salida1}')
    print(f'   - {archivo_salida2}')
    print(f'✓ Total de himnos extraídos: {len(himnos)}')
    if inconsistencias:
        print('⚠ Revisa las inconsistencias antes de continuar')
    print('=' * 80)

if __name__ == '__main__':
    main()
