"""
GENERAR_PDF_HIMNARIO.PY
=======================
Genera un PDF profesional listo para impresión a partir de Himnario_Limpio_Final.txt.
- Portada profesional
- Índice alfabético
- Himnos en dos columnas
- Títulos destacados
- Estrofas separadas e indentadas
- Coros resaltados y numerados
- Numeración de página en el pie

Uso:
    python generar_pdf_himnario.py

Dependencia:
    pip install reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Frame, PageTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import mm
import os
import re

# Configuración
PAGE_SIZE = A4
MARGINS = (20*mm, 20*mm, 20*mm, 20*mm)  # left, right, top, bottom
COLUMN_GAP = 10*mm
FONT_MAIN = 'Times-Roman'
FONT_TITLE = 'Times-Bold'
FONT_CHORUS = 'Times-BoldItalic'

# Estilos
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='HimnoTitulo', fontName=FONT_TITLE, fontSize=12, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(name='Estrofa', fontName=FONT_MAIN, fontSize=10, leftIndent=10, spaceAfter=4))
styles.add(ParagraphStyle(name='Coro', fontName=FONT_CHORUS, fontSize=10, leftIndent=20, textColor=colors.darkblue, spaceAfter=4))
styles.add(ParagraphStyle(name='Indice', fontName=FONT_MAIN, fontSize=9, leftIndent=0, spaceAfter=2))

# Portada profesional
def portada_profesional():
    portada = []
    portada.append(Spacer(1, 40*mm))
    portada.append(Paragraph('<font size=32><b>Himnario Tabernáculo La Esperanza</b></font>', styles['Title']))
    portada.append(Spacer(1, 10*mm))
    portada.append(Paragraph('<font size=18>Un nuevo amanecer</font>', styles['Title']))
    portada.append(Spacer(1, 20*mm))
    portada.append(Paragraph('<font size=14>Compilación y edición: Equipo de Música</font>', styles['Normal']))
    portada.append(Spacer(1, 10*mm))
    portada.append(Paragraph('<font size=14>Año: 2026</font>', styles['Normal']))
    portada.append(Spacer(1, 60*mm))
    portada.append(Paragraph('<font size=12>Listo para impresión profesional</font>', styles['Normal']))
    portada.append(PageBreak())
    return portada

# Numeración de página
def agregar_numeracion(canvas, doc):
    if doc.page > 1:  # No numerar portada
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawCentredString(PAGE_SIZE[0]/2, 12*mm, f"Página {doc.page}")
        canvas.restoreState()

# Parseo de himnos
def parsear_himnos(path):
    patron = r'(\d+)\.\s+(.+?)\n((?:(?!\n\d+\.\s).)+)'
    with open(path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    return re.findall(patron, contenido, re.DOTALL)

def crear_indice(himnos):
    lista = sorted([(t.strip(), n) for n, t, l in himnos], key=lambda x: x[0].lower())
    parrafos = [Paragraph(f"{n}. {t}", styles['Indice']) for t, n in lista]
    return parrafos

def procesar_letra(letra):
    bloques = letra.strip().split('\n\n')
    parrafos = []
    coro_num = 1
    for bloque in bloques:
        lineas = bloque.strip().split('\n')
        if lineas and re.match(r'^(coro|estribillo|final)', lineas[0].lower()):
            # Coro numerado si corresponde
            if re.match(r'^coro', lineas[0].lower()):
                parrafos.append(Paragraph(f'<b>Coro {coro_num}</b>', styles['Coro']))
                coro_num += 1
            else:
                parrafos.append(Paragraph('<b>' + lineas[0] + '</b>', styles['Coro']))
            for linea in lineas[1:]:
                parrafos.append(Paragraph(linea, styles['Coro']))
        else:
            for linea in lineas:
                parrafos.append(Paragraph(linea, styles['Estrofa']))
    return parrafos

def crear_himno(num, titulo, letra):
    out = [Paragraph(f"{num}. {titulo}", styles['HimnoTitulo'])]
    out += procesar_letra(letra)
    out.append(Spacer(1, 8))
    return out

def main():
    post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
    archivo_entrada = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
    archivo_pdf = os.path.join(post_dir, 'Himnario_TabernaculoLaEsperanza_V1.pdf')
    archivo_indice = os.path.join(post_dir, 'Indice_Alfabetico_Final.txt')

    print('='*80)
    print('GENERADOR DE HIMNARIO PDF PROFESIONAL')
    print('='*80)
    print('[1/5] Leyendo himnos...')
    himnos = parsear_himnos(archivo_entrada)
    print(f'      Total de himnos: {len(himnos)}')

    print('[2/5] Generando portada profesional...')
    portada = portada_profesional()

    print('[3/5] Generando índice alfabético...')
    indice = crear_indice(himnos)
    indice.insert(0, Paragraph('<b>ÍNDICE ALFABÉTICO</b>', styles['Title']))
    indice.append(PageBreak())

    print('[4/5] Procesando himnos y formato...')
    contenido = []
    for num, titulo, letra in himnos:
        contenido += crear_himno(num, titulo, letra)
        contenido.append(Spacer(1, 10))
    print('[5/5] Generando PDF...')
    doc = SimpleDocTemplate(
        archivo_pdf,
        pagesize=PAGE_SIZE,
        leftMargin=MARGINS[0],
        rightMargin=MARGINS[1],
        topMargin=MARGINS[2],
        bottomMargin=MARGINS[3],
        title="Himnario Tabernáculo La Esperanza",
        author="Equipo de Música"
    )
    # Dos columnas
    frame1 = Frame(MARGINS[0], MARGINS[3], (PAGE_SIZE[0]-MARGINS[0]-MARGINS[1]-COLUMN_GAP)/2, PAGE_SIZE[1]-MARGINS[2]-MARGINS[3], leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    frame2 = Frame(MARGINS[0]+(PAGE_SIZE[0]-MARGINS[0]-MARGINS[1]-COLUMN_GAP)/2+COLUMN_GAP, MARGINS[3], (PAGE_SIZE[0]-MARGINS[0]-MARGINS[1]-COLUMN_GAP)/2, PAGE_SIZE[1]-MARGINS[2]-MARGINS[3], leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    template = PageTemplate(frames=[frame1, frame2], onPage=agregar_numeracion)
    doc.addPageTemplates([template])
    story = portada + indice + contenido
    doc.build(story)
    print(f'OK PDF generado: {archivo_pdf}')
    print('='*80)

if __name__ == '__main__':
    main()
"""
GENERAR_PDF_HIMNARIO.PY
=======================
Genera un PDF profesional listo para impresión a partir de Himnario_Limpio_Final.txt.
- Portada personalizada
- Índice alfabético
- Himnos en dos columnas
- Títulos destacados
- Estrofas separadas e indentadas
- Coros resaltados
- Saltos de página automáticos

Uso:
    python generar_pdf_himnario.py

Dependencia:
    pip install reportlab
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Frame, PageTemplate, NextPageTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import mm
import os
import re

# Configuración
PAGE_SIZE = A4
MARGINS = (20*mm, 20*mm, 20*mm, 20*mm)  # left, right, top, bottom
COLUMN_GAP = 10*mm
FONT_MAIN = 'Times-Roman'
FONT_TITLE = 'Times-Bold'
FONT_CHORUS = 'Times-BoldItalic'

# Portada
PORTADA = [
    Paragraph('<font size=24><b>Himnario Tabernáculo La Esperanza</b></font>', getSampleStyleSheet()['Title']),
    Spacer(1, 20*mm),
    Paragraph('<font size=16>Compilación y edición: Equipo de Música</font>', getSampleStyleSheet()['Normal']),
    Spacer(1, 10*mm),
    Paragraph('<font size=14>Año: 2026</font>', getSampleStyleSheet()['Normal']),
    Spacer(1, 60*mm),
    Paragraph('<font size=12>Listo para impresión profesional</font>', getSampleStyleSheet()['Normal']),
    PageBreak()
]

# Estilos
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='HimnoTitulo', fontName=FONT_TITLE, fontSize=12, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(name='Estrofa', fontName=FONT_MAIN, fontSize=10, leftIndent=10, spaceAfter=4))
styles.add(ParagraphStyle(name='Coro', fontName=FONT_CHORUS, fontSize=10, leftIndent=20, textColor=colors.darkblue, spaceAfter=4))
styles.add(ParagraphStyle(name='Indice', fontName=FONT_MAIN, fontSize=9, leftIndent=0, spaceAfter=2))

# Funciones

def parsear_himnos(path):
    """Devuelve lista de himnos: [(num, titulo, letra)]"""
    patron = r'(\d+)\.\s+(.+?)\n((?:(?!\n\d+\.\s).)+)'
    with open(path, 'r', encoding='utf-8') as f:
        contenido = f.read()
    return re.findall(patron, contenido, re.DOTALL)

def crear_indice(himnos):
    """Devuelve lista de Paragraphs para el índice alfabético"""
    lista = sorted([(t.strip(), n) for n, t, l in himnos], key=lambda x: x[0].lower())
    parrafos = [Paragraph(f"{n}. {t}", styles['Indice']) for t, n in lista]
    return parrafos

def procesar_letra(letra):
    """Convierte letra en lista de Paragraphs, separando estrofas y coros"""
    bloques = letra.strip().split('\n\n')
    parrafos = []
    for bloque in bloques:
        lineas = bloque.strip().split('\n')
        if lineas and re.match(r'^(coro|estribillo|final)', lineas[0].lower()):
            parrafos.append(Paragraph('<b>' + lineas[0] + '</b>', styles['Coro']))
            for linea in lineas[1:]:
                parrafos.append(Paragraph(linea, styles['Coro']))
        else:
            for linea in lineas:
                parrafos.append(Paragraph(linea, styles['Estrofa']))
    return parrafos

def crear_himno(num, titulo, letra):
    """Devuelve lista de Paragraphs para un himno completo"""
    out = [Paragraph(f"{num}. {titulo}", styles['HimnoTitulo'])]
    out += procesar_letra(letra)
    out.append(Spacer(1, 8))
    return out

def main():
    post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
    archivo_entrada = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
    archivo_pdf = os.path.join(post_dir, 'Himnario_TabernaculoLaEsperanza_V1.pdf')
    archivo_indice = os.path.join(post_dir, 'Indice_Alfabetico_Final.txt')

    print('='*80)
    print('GENERADOR DE HIMNARIO PDF PROFESIONAL')
    print('='*80)
    print('[1/5] Leyendo himnos...')
    himnos = parsear_himnos(archivo_entrada)
    print(f'      Total de himnos: {len(himnos)}')

    print('[2/5] Generando portada...')
    portada = PORTADA

    print('[3/5] Generando índice alfabético...')
    indice = crear_indice(himnos)
    indice.insert(0, Paragraph('<b>ÍNDICE ALFABÉTICO</b>', styles['Title']))
    indice.append(PageBreak())

    print('[4/5] Procesando himnos y formato...')
    contenido = []
    for num, titulo, letra in himnos:
        contenido += crear_himno(num, titulo, letra)
        contenido.append(Spacer(1, 10))
    print('[5/5] Generando PDF...')
    doc = SimpleDocTemplate(
        archivo_pdf,
        pagesize=PAGE_SIZE,
        leftMargin=MARGINS[0],
        rightMargin=MARGINS[1],
        topMargin=MARGINS[2],
        bottomMargin=MARGINS[3],
        title="Himnario Tabernáculo La Esperanza",
        author="Equipo de Música"
    )
    # Dos columnas
    frame1 = Frame(MARGINS[0], MARGINS[3], (PAGE_SIZE[0]-MARGINS[0]-MARGINS[1]-COLUMN_GAP)/2, PAGE_SIZE[1]-MARGINS[2]-MARGINS[3], leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    frame2 = Frame(MARGINS[0]+(PAGE_SIZE[0]-MARGINS[0]-MARGINS[1]-COLUMN_GAP)/2+COLUMN_GAP, MARGINS[3], (PAGE_SIZE[0]-MARGINS[0]-MARGINS[1]-COLUMN_GAP)/2, PAGE_SIZE[1]-MARGINS[2]-MARGINS[3], leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0)
    template = PageTemplate(frames=[frame1, frame2])
    doc.addPageTemplates([template])
    story = portada + indice + contenido
    doc.build(story)
    print(f'OK PDF generado: {archivo_pdf}')
    print('='*80)

if __name__ == '__main__':
    main()
