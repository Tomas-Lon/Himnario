"""
ORDENAR_ALFABETICO.PY
=====================
Ordena los himnos alfabéticamente usando normalización Unicode
para manejar correctamente tildes y caracteres especiales.

Normalización:
- á, é, í, ó, ú → a, e, i, o, u
- Ignora contenido entre paréntesis
- Case-insensitive

Genera:
- Himnario_Limpio_Final.txt (ordenado)
- Indice_Alfabetico_Final.txt
- REPORTE_REORDENAMIENTO.txt

Uso:
    python ordenar_alfabetico.py
"""

import re
import unicodedata

def normalizar_para_orden(titulo):
    """
    Normaliza título para ordenamiento alfabético
    - Remueve tildes usando NFD
    - Convierte a minúsculas
    - Ignora contenido entre paréntesis
    """
    # Remover contenido entre paréntesis
    titulo_limpio = re.sub(r'\([^)]*\)', '', titulo).strip()
    
    # Normalizar Unicode (separar caracteres base de diacríticos)
    nfd = unicodedata.normalize('NFD', titulo_limpio)
    
    # Remover diacríticos y convertir a minúsculas
    sin_tildes = ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
    
    return sin_tildes.lower()

def parsear_himnario(contenido):
    """Extrae todos los himnos del archivo"""
    patron = r'(\d+)\.\s+(.+?)\n((?:(?!\n\d+\.\s).)+)'
    return re.findall(patron, contenido, re.DOTALL)

def main():
    """Función principal"""
    print('=' * 80)
    print('ORDENAMIENTO ALFABÉTICO DE HIMNOS')
    print('=' * 80)
    
    # Leer archivo
    print('\n[1/4] Leyendo Himnario_Limpio_Final.txt de post-proceso/...')
    import os
    post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
    archivo_path = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
    archivo_indice = os.path.join(post_dir, 'Indice_Alfabetico_Final.txt')
    archivo_reporte = os.path.join(post_dir, 'REPORTE_REORDENAMIENTO.txt')
    with open(archivo_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Parsear himnos
    print('[2/4] Parseando himnos...')
    himnos = parsear_himnario(contenido)
    print(f'      Total de himnos: {len(himnos)}')
    
    # Crear lista ordenada
    print('[3/4] Ordenando alfabéticamente...')
    himnos_con_clave = []
    for num_orig, titulo, letra in himnos:
        clave_orden = normalizar_para_orden(titulo)
        himnos_con_clave.append({
            'num_original': int(num_orig),
            'titulo': titulo.strip(),
            'letra': letra,
            'clave': clave_orden
        })
    
    # Ordenar por clave
    himnos_ordenados = sorted(himnos_con_clave, key=lambda x: x['clave'])
    
    # Detectar cambios
    cambios = []
    for nuevo_num, himno in enumerate(himnos_ordenados, 1):
        if himno['num_original'] != nuevo_num:
            cambios.append({
                'titulo': himno['titulo'],
                'num_viejo': himno['num_original'],
                'num_nuevo': nuevo_num
            })
    
    print(f'      Himnos que cambiaron de número: {len(cambios)}')
    print(f'      Himnos que mantuvieron su posición: {len(himnos) - len(cambios)}')
    
    # Guardar archivo ordenado
    print('[4/4] Guardando archivos en post-proceso/...')
    # Himnario ordenado
    with open(archivo_path, 'w', encoding='utf-8') as f:
        for nuevo_num, himno in enumerate(himnos_ordenados, 1):
            f.write(f"{nuevo_num}. {himno['titulo']}\n")
            f.write(f"{himno['letra']}\n\n")
    # Índice alfabético
    with open(archivo_indice, 'w', encoding='utf-8') as f:
        f.write('ÍNDICE ALFABÉTICO DEL HIMNARIO\n')
        f.write('=' * 80 + '\n\n')
        for nuevo_num, himno in enumerate(himnos_ordenados, 1):
            f.write(f"{nuevo_num:3d}. {himno['titulo']}\n")
    # Reporte de cambios
    with open(archivo_reporte, 'w', encoding='utf-8') as f:
        f.write('=' * 80 + '\n')
        f.write('REPORTE DE REORDENAMIENTO ALFABÉTICO\n')
        f.write('=' * 80 + '\n\n')
        f.write(f'Total de himnos: {len(himnos)}\n')
        f.write(f'Himnos que cambiaron de número: {len(cambios)}\n')
        f.write(f'Himnos que mantuvieron su posición: {len(himnos) - len(cambios)}\n\n')
        if cambios:
            f.write('=' * 80 + '\n')
            f.write('DETALLE DE CAMBIOS\n')
            f.write('=' * 80 + '\n\n')
            for cambio in cambios:
                f.write(f"#{cambio['num_viejo']:3d} → #{cambio['num_nuevo']:3d}  |  {cambio['titulo']}\n")
        f.write('\n' + '=' * 80 + '\n')
        f.write('ÍNDICE COMPLETO (ORDEN ALFABÉTICO)\n')
        f.write('=' * 80 + '\n\n')
        for nuevo_num, himno in enumerate(himnos_ordenados, 1):
            f.write(f"{nuevo_num:3d}. {himno['titulo']}\n")
    
    print('\n' + '=' * 80)
    print('OK Archivos generados:')
    print('  - Himnario_Limpio_Final.txt (ordenado alfabéticamente)')
    print('  - Indice_Alfabetico_Final.txt')
    print('  - REPORTE_REORDENAMIENTO.txt')
    print(f'\nOK Cambios: {len(cambios)} himnos renumerados')
    print('=' * 80)

if __name__ == '__main__':
    main()
