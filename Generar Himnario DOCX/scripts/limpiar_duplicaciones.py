"""
LIMPIAR DUPLICACIONES
======================
Elimina palabras duplicadas tipo "jesúsJesús", "élÉl", etc.
"""

import re

def limpiar_duplicaciones(texto):
    """Elimina duplicaciones de palabras divinas"""
    # Patrones de duplicación
    patrones = [
        (r'jesúsJesús', 'Jesús'),
        (r'diosDios', 'Dios'),
        (r'señorSeñor', 'Señor'),
        (r'cristoCristo', 'Cristo'),
        (r'élÉl', 'Él'),
        (r'jehováJehová', 'Jehová'),
    ]
    
    for patron, reemplazo in patrones:
        texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE)
    
    return texto

def main():
    print('=' * 80)
    print('LIMPIEZA DE DUPLICACIONES')
    print('=' * 80)
    
    # Leer archivo
    print('\n[1/2] Leyendo Himnario_Limpio_Final.txt de post-proceso/...')
    import os
    post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
    archivo_path = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
    with open(archivo_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Limpiar duplicaciones
    print('[2/2] Eliminando duplicaciones...')
    contenido_limpio = limpiar_duplicaciones(contenido)
    
    # Contar cambios
    cambios = len(re.findall(r'(jesúsJesús|diosDios|señorSeñor|cristoCristo|élÉl|jehováJehová)', contenido, re.IGNORECASE))
    
    # Guardar
    with open(archivo_path, 'w', encoding='utf-8') as f:
        f.write(contenido_limpio)
    
    print('\n' + '=' * 80)
    print(f'OK Duplicaciones eliminadas: {cambios}')
    print('OK Archivo actualizado: Himnario_Limpio_Final.txt')
    print('=' * 80)

if __name__ == '__main__':
    main()
