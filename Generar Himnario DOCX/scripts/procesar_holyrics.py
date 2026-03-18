"""
PROCESAR_HOLYRICS.PY
====================
Procesa archivos JSON exportados de Holyrics aplicando las mismas
reglas de formato que usa procesar_formato.py

Aplica:
- Formato tipo oración
- Capitalización de nombres divinos
- Normalización de CORO/ESTRIBILLO
- Detección de texto en mayúsculas

Uso:
    1. Exporta himnos desde Holyrics en formato JSON
    2. Ejecuta: python procesar_holyrics.py
    3. Importa el archivo holyrics_procesado.json de vuelta a Holyrics

Entrada:
    Archivo JSON de Holyrics (solicita nombre)
    
Salida:
    holyrics_procesado.json
    REPORTE_CAMBIOS_HOLYRICS.txt
"""

import json
import re
import os

# Importar funciones del procesador de formato
from procesar_formato import (
    PALABRAS_ESPECIALES,
    esta_en_mayusculas,
    capitalizar_oracion,
    es_marcador_coro,
    normalizar_marcador_coro,
    capitalizar_palabra_especial
)

def procesar_parrafo(texto):
    """Procesa un párrafo de texto"""
    # No modificar marcadores de CORO
    if es_marcador_coro(texto.strip()):
        return normalizar_marcador_coro(texto)
    
    # Convertir si está en mayúsculas
    if esta_en_mayusculas(texto):
        texto = texto.lower()
    
    # Procesar línea por línea
    lineas = texto.split('\n')
    lineas_procesadas = []
    
    for linea in lineas:
        if linea.strip():
            if es_marcador_coro(linea):
                lineas_procesadas.append(normalizar_marcador_coro(linea))
            else:
                lineas_procesadas.append(capitalizar_oracion(linea))
        else:
            lineas_procesadas.append(linea)
    
    return '\n'.join(lineas_procesadas)

def procesar_titulo(titulo):
    """Procesa título capitalizando palabras importantes"""
    # Remover numeración inicial
    titulo_limpio = re.sub(r'^\d+\.?\s*', '', titulo).strip()
    
    palabras = titulo_limpio.split()
    resultado = []
    
    for palabra in palabras:
        palabra_limpia = palabra.lower().strip('.,;:!?¡¿()[]{}"\'')
        if palabra_limpia in PALABRAS_ESPECIALES:
            resultado.append(capitalizar_palabra_especial(palabra))
        else:
            resultado.append(palabra[0].upper() + palabra[1:] if len(palabra) > 0 else palabra)
    
    return ' '.join(resultado)

def procesar_himno(himno):
    """Procesa un himno completo de Holyrics"""
    cambios = []
    
    # Procesar título
    if 'title' in himno and himno['title']:
        titulo_original = himno['title']
        titulo_procesado = procesar_titulo(titulo_original)
        if titulo_original != titulo_procesado:
            cambios.append(f"Título: '{titulo_original}' → '{titulo_procesado}'")
        himno['title'] = titulo_procesado
    
    # Procesar lyrics
    if 'lyrics' in himno and himno['lyrics']:
        # Procesar full_text
        if 'full_text' in himno['lyrics'] and himno['lyrics']['full_text']:
            texto_original = himno['lyrics']['full_text']
            parrafos = texto_original.split('\n\n')
            parrafos_procesados = [procesar_parrafo(p) for p in parrafos]
            texto_procesado = '\n\n'.join(parrafos_procesados)
            
            if texto_original != texto_procesado:
                cambios.append("Texto modificado")
            
            himno['lyrics']['full_text'] = texto_procesado
        
        # Procesar paragraphs
        if 'paragraphs' in himno['lyrics'] and himno['lyrics']['paragraphs']:
            for parrafo in himno['lyrics']['paragraphs']:
                if 'text' in parrafo and parrafo['text']:
                    parrafo['text'] = procesar_parrafo(parrafo['text'])
    
    return cambios

def main():
    """Función principal"""
    print('=' * 80)
    print('PROCESADOR DE ARCHIVOS HOLYRICS JSON')
    print('=' * 80)
    
    # Listar archivos JSON disponibles
    print('\nArchivos JSON disponibles:')
    archivos_json = [f for f in os.listdir('.') if f.endswith('.json') and 'procesado' not in f.lower()]
    
    if not archivos_json:
        print('⚠ No se encontraron archivos JSON en la carpeta')
        return
    
    for i, archivo in enumerate(archivos_json, 1):
        print(f'{i}. {archivo}')
    
    seleccion = input('\nSelecciona el número de archivo a procesar: ')
    try:
        archivo_input = archivos_json[int(seleccion) - 1]
    except (ValueError, IndexError):
        print('⚠ Selección inválida')
        return
    
    # Leer archivo JSON
    print(f'\n[1/3] Leyendo {archivo_input}...')
    with open(archivo_input, 'r', encoding='utf-8') as f:
        himnos = json.load(f)
    
    print(f'      Total de himnos: {len(himnos)}')
    
    # Procesar cada himno
    print('[2/3] Procesando himnos...')
    reporte_cambios = []
    
    for i, himno in enumerate(himnos, 1):
        try:
            cambios = procesar_himno(himno)
            if cambios:
                titulo = himno.get('title', 'SIN TÍTULO')
                reporte_cambios.append({
                    'numero': i,
                    'titulo': titulo,
                    'cambios': cambios
                })
        except Exception as e:
            print(f"      ⚠ Error en himno #{i}: {str(e)}")
    
    print(f'      Himnos modificados: {len(reporte_cambios)}')
    
    # Guardar archivos
    print('[3/3] Guardando archivos...')
    
    # JSON procesado
    with open('holyrics_procesado.json', 'w', encoding='utf-8') as f:
        json.dump(himnos, f, ensure_ascii=False, indent=2)
    
    # Reporte de cambios
    with open('REPORTE_CAMBIOS_HOLYRICS.txt', 'w', encoding='utf-8') as f:
        f.write('=' * 80 + '\n')
        f.write('REPORTE DE PROCESAMIENTO HOLYRICS\n')
        f.write('=' * 80 + '\n\n')
        f.write(f'Archivo procesado: {archivo_input}\n')
        f.write(f'Total de himnos: {len(himnos)}\n')
        f.write(f'Himnos modificados: {len(reporte_cambios)}\n\n')
        
        if reporte_cambios:
            f.write('=' * 80 + '\n')
            f.write('DETALLE DE CAMBIOS\n')
            f.write('=' * 80 + '\n\n')
            for item in reporte_cambios:
                f.write(f"Himno #{item['numero']}: {item['titulo']}\n")
                for cambio in item['cambios']:
                    f.write(f"  - {cambio}\n")
                f.write('\n')
    
    print('\n' + '=' * 80)
    print('✓ Archivos generados:')
    print('  - holyrics_procesado.json (listo para importar)')
    print('  - REPORTE_CAMBIOS_HOLYRICS.txt')
    print(f'\n✓ Total de cambios: {len(reporte_cambios)}')
    print('=' * 80)

if __name__ == '__main__':
    main()
