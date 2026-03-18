"""
GENERAR_JSON_HOLYRICS.PY
========================
Convierte Himnario_Limpio_Final.txt al formato JSON de Holyrics
para importación masiva de todos los himnos.

Formato de salida: JSON compatible con Holyrics 2.x+

Uso:
    python generar_json_holyrics.py
    
Salida:
    Himnario_Completo_Holyrics.json (listo para importar)
"""

import json
import re

def dividir_en_parrafos(letra):
    """Divide la letra en párrafos detectando líneas vacías"""
    parrafos_raw = letra.strip().split('\n\n')
    parrafos = []
    
    for i, p in enumerate(parrafos_raw, 1):
        if p.strip():
            parrafos.append({
                "number": i,
                "description": "",
                "text": p.strip(),
                "text_with_comment": None,
                "translations": None
            })
    
    return parrafos

def crear_estructura_himno(numero, titulo, letra):
    """Crea la estructura JSON compatible con Holyrics"""
    base_id = 1700000000000
    himno_id = base_id + int(numero)
    
    return {
        "id": himno_id,
        "title": f"{numero}. {titulo.strip()}",
        "artist": "",
        "author": "",
        "note": "",
        "copyright": "",
        "key": "",
        "bpm": 0.0,
        "time_sig": "",
        "midi": None,
        "order": "",
        "arrangements": [],
        "lyrics": {
            "full_text": letra.strip(),
            "full_text_with_comment": None,
            "paragraphs": dividir_en_parrafos(letra)
        },
        "streaming": {
            "audio": {
                "spotify": "",
                "youtube": "",
                "deezer": ""
            },
            "backing_track": {
                "spotify": "",
                "youtube": "",
                "deezer": ""
            }
        },
        "extras": {
            "extra": ""
        }
    }

def main():
    """Función principal"""
    print('=' * 80)
    print('GENERADOR JSON PARA HOLYRICS')
    print('=' * 80)
    
    # Leer archivo fuente
    print('\n[1/3] Leyendo Himnario_Limpio_Final.txt de post-proceso/...')
    import os
    post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
    archivo_entrada = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
    archivo_salida = os.path.join(post_dir, 'Himnario_Completo_Holyrics.json')
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Parsear himnos
    print('[2/3] Procesando himnos...')
    patron = r'(\d+)\.\s+(.+?)\n((?:(?!\n\d+\.\s).)+)'
    matches = re.findall(patron, contenido, re.DOTALL)
    print(f'      Total de himnos encontrados: {len(matches)}')
    
    # Generar estructura JSON
    print('[3/3] Generando estructura JSON...')
    himnos_json = []
    
    for numero, titulo, letra in matches:
        try:
            himno = crear_estructura_himno(numero, titulo, letra)
            himnos_json.append(himno)
        except Exception as e:
            print(f'      ⚠ Error procesando himno {numero}: {str(e)}')
    
    # Guardar JSON
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(himnos_json, f, ensure_ascii=False, indent=2)
    
    print('\n' + '=' * 80)
    print(f'OK Archivo JSON generado: {archivo_salida}')
    print(f'OK Total de himnos: {len(himnos_json)}')
    print('=' * 80)
    print('\nINSTRUCCIONES PARA IMPORTAR EN HOLYRICS:')
    print('1. Abre Holyrics')
    print('2. Ve a Archivo > Importar (o Herramientas > Importar)')
    print(f'3. Selecciona: {archivo_salida}')
    print('4. Elige "Agregar/Actualizar" o "Reemplazar todo"')
    print('5. Confirma la importación')
    print('\nIMPORTANTE: Haz un respaldo antes de importar!')
    print('=' * 80)

if __name__ == '__main__':
    main()
