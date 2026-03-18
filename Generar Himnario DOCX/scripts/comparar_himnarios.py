"""
COMPARAR_HIMNARIOS.PY
=====================
Compara dos versiones de himnarios y genera un reporte detallado
de las diferencias encontradas.

Compara:
- Títulos
- Contenido (letra)
- Cantidad de himnos
- Coincidencias y diferencias

Uso:
    python comparar_himnarios.py

Salida:
    REPORTE_COMPARACION.txt
"""

import re
from difflib import SequenceMatcher

def parsear_himnario(ruta_archivo):
    """Lee y parsea un archivo de himnario"""
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        patron = r'(\d+)\.\s+(.+?)\n((?:(?!\n\d+\.\s).)+)'
        himnos = re.findall(patron, contenido, re.DOTALL)
        
        resultado = {}
        for num, titulo, letra in himnos:
            resultado[int(num)] = {
                'titulo': titulo.strip(),
                'letra': letra.strip()
            }
        
        return resultado
    except Exception as e:
        print(f'⚠ Error leyendo {ruta_archivo}: {str(e)}')
        return {}

def calcular_similitud(texto1, texto2):
    """Calcula porcentaje de similitud entre dos textos"""
    return SequenceMatcher(None, texto1, texto2).ratio() * 100

def comparar_himnarios(himnario1, himnario2, nombre1, nombre2):
    """Compara dos himnarios y retorna reporte de diferencias"""
    reporte = []
    reporte.append('=' * 80)
    reporte.append(f'COMPARACIÓN DE HIMNARIOS')
    reporte.append('=' * 80)
    reporte.append(f'\nArchivo 1: {nombre1}')
    reporte.append(f'Total de himnos: {len(himnario1)}')
    reporte.append(f'\nArchivo 2: {nombre2}')
    reporte.append(f'Total de himnos: {len(himnario2)}')
    
    # Encontrar números en común
    nums1 = set(himnario1.keys())
    nums2 = set(himnario2.keys())
    
    comunes = nums1 & nums2
    solo_en_1 = nums1 - nums2
    solo_en_2 = nums2 - nums1
    
    reporte.append(f'\nHimnos en común: {len(comunes)}')
    reporte.append(f'Solo en {nombre1}: {len(solo_en_1)}')
    reporte.append(f'Solo en {nombre2}: {len(solo_en_2)}')
    
    # Analizar diferencias en himnos comunes
    titulos_diferentes = []
    letras_diferentes = []
    
    for num in sorted(comunes):
        h1 = himnario1[num]
        h2 = himnario2[num]
        
        # Comparar títulos
        if h1['titulo'].lower() != h2['titulo'].lower():
            titulos_diferentes.append({
                'num': num,
                'titulo1': h1['titulo'],
                'titulo2': h2['titulo']
            })
        
        # Comparar letras
        if h1['letra'] != h2['letra']:
            similitud = calcular_similitud(h1['letra'], h2['letra'])
            letras_diferentes.append({
                'num': num,
                'titulo': h1['titulo'],
                'similitud': similitud
            })
    
    reporte.append(f'\nTítulos diferentes: {len(titulos_diferentes)}')
    reporte.append(f'Letras diferentes: {len(letras_diferentes)}')
    
    # Detallar títulos diferentes
    if titulos_diferentes:
        reporte.append('\n' + '=' * 80)
        reporte.append('TÍTULOS DIFERENTES')
        reporte.append('=' * 80)
        for item in titulos_diferentes:
            reporte.append(f"\nHimno #{item['num']}:")
            reporte.append(f"  {nombre1}: {item['titulo1']}")
            reporte.append(f"  {nombre2}: {item['titulo2']}")
    
    # Detallar letras diferentes
    if letras_diferentes:
        reporte.append('\n' + '=' * 80)
        reporte.append('LETRAS DIFERENTES')
        reporte.append('=' * 80)
        for item in letras_diferentes:
            reporte.append(f"\nHimno #{item['num']}: {item['titulo']}")
            reporte.append(f"  Similitud: {item['similitud']:.1f}%")
    
    # Listar himnos solo en archivo 1
    if solo_en_1:
        reporte.append('\n' + '=' * 80)
        reporte.append(f'HIMNOS SOLO EN {nombre1}')
        reporte.append('=' * 80)
        for num in sorted(solo_en_1):
            reporte.append(f"#{num}: {himnario1[num]['titulo']}")
    
    # Listar himnos solo en archivo 2
    if solo_en_2:
        reporte.append('\n' + '=' * 80)
        reporte.append(f'HIMNOS SOLO EN {nombre2}')
        reporte.append('=' * 80)
        for num in sorted(solo_en_2):
            reporte.append(f"#{num}: {himnario2[num]['titulo']}")
    
    return '\n'.join(reporte)

def main():
    """Función principal"""
    print('=' * 80)
    print('COMPARADOR DE HIMNARIOS')
    print('=' * 80)
    
    # Listar archivos TXT disponibles
    import os
    archivos_txt = [f for f in os.listdir('.') if f.endswith('.txt') and 'REPORTE' not in f and 'Indice' not in f]
    
    if len(archivos_txt) < 2:
        print('\n⚠ Se necesitan al menos 2 archivos .txt para comparar')
        return
    
    print('\nArchivos disponibles:')
    for i, archivo in enumerate(archivos_txt, 1):
        print(f'{i}. {archivo}')
    
    # Seleccionar primer archivo
    sel1 = input('\nSelecciona el primer archivo (número): ')
    try:
        archivo1 = archivos_txt[int(sel1) - 1]
    except (ValueError, IndexError):
        print('⚠ Selección inválida')
        return
    
    # Seleccionar segundo archivo
    sel2 = input('Selecciona el segundo archivo (número): ')
    try:
        archivo2 = archivos_txt[int(sel2) - 1]
    except (ValueError, IndexError):
        print('⚠ Selección inválida')
        return
    
    if archivo1 == archivo2:
        print('⚠ Debes seleccionar dos archivos diferentes')
        return
    
    # Parsear himnarios
    print(f'\n[1/3] Leyendo {archivo1}...')
    himnario1 = parsear_himnario(archivo1)
    
    print(f'[2/3] Leyendo {archivo2}...')
    himnario2 = parsear_himnario(archivo2)
    
    # Comparar
    print('[3/3] Comparando himnarios...')
    reporte = comparar_himnarios(himnario1, himnario2, archivo1, archivo2)
    
    # Guardar reporte
    archivo_salida = 'REPORTE_COMPARACION.txt'
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(reporte)
    
    print('\n' + '=' * 80)
    print(f'✓ Reporte generado: {archivo_salida}')
    print('=' * 80)
    
    # Mostrar resumen
    print('\nRESUMEN:')
    print(reporte.split('=' * 80)[1])

if __name__ == '__main__':
    main()
