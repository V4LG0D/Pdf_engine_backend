import fitz  # PyMuPDF
import os
from pdf2docx import Converter
from docx import Document
from spellchecker import SpellChecker
import wordninja
import re

def move_body_table_to_header(docx_path):
    """
    Busca la tabla del encabezado en el cuerpo principal, la extrae 
    y la inserta en el encabezado nativo de Word a nivel de XML.
    """
    doc = Document(docx_path)
    target_text = "Universidad Autónoma del Estado d México"
    
    table_to_move = None
    target_index = -1
    
    # 1. Localizar la tabla que contiene el encabezado en el cuerpo
    for i, table in enumerate(doc.tables):
        table_text = "".join([cell.text for row in table.rows for cell in row.cells])
        if target_text in table_text:
            table_to_move = table
            break
            
    if table_to_move:
        # 2. Obtener el elemento XML raíz de la tabla (<w:tbl>)
        tbl_element = table_to_move._element
        
        # 3. Desconectar la tabla de su padre actual en el cuerpo del documento
        parent = tbl_element.getparent()
        parent.remove(tbl_element)
        
        # 4. Obtener el contenedor XML del encabezado de la primera sección (<w:hdr>)
        section = doc.sections[0]
        header = section.header
        header_element = header._element 
        
        # Opcional: Limpiar párrafos vacíos previos en el encabezado nativo si los hubiera
        for child in list(header_element):
            if child.tag.endswith('p'): # Si es un párrafo vacío por defecto
                header_element.remove(child)
                
        # 5. Inyectar la tabla completa (con imagen, líneas y formato) en el encabezado
        header_element.append(tbl_element)
        
    doc.save(docx_path)

def fix_glued_words(text: str) -> str:
    """Aplica NLP para separar palabras pegadas erróneamente."""
    spell = SpellChecker(language='es') 
    words = text.split()
    corrected_text = []
    
    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word)
        
        if not spell.known([clean_word]) or len(clean_word) > 15:
            separated = " ".join(wordninja.split(word))
            corrected_text.append(separated)
        else:
            corrected_text.append(word)
            
    return " ".join(corrected_text)

def fix_latex_accents_in_docx(docx_path, output_path=None):
    """
    Abre un documento Word, corrige los acentos separados típicos de LaTeX
    y guarda el resultado conservando el formato original en los runs.
    """
    if output_path is None:
        output_path = docx_path 
    
    replacements = {
        "´a": "á", "´e": "é", "´i": "í", "´o": "ó", "´u": "ú",
        "´A": "Á", "´E": "É", "´I": "Í", "´O": "Ó", "´U": "Ú",
        "´ a": "á", "´ e": "é", "´ i": "í", "´ o": "ó", "´ u": "ú",
        "´ı": "í", "´ ı": "í",
        "\\'a": "á", "\\'e": "é", "\\'i": "í", "\\'o": "ó", "\\'u": "ú",
        "\\`a": "à", "\\`e": "è", "\\`i": "ì", "\\`o": "ò", "\\`u": "ù",
        "\\~n": "ñ", "\\~a": "ã", "\\~o": "õ",
        "\\\"a": "ä", "\\\"e": "ë", "\\\"i": "ï", "\\\"o": "ö", "\\\"u": "ü",
        "\\^a": "â", "\\^e": "ê", "\\^i": "î", "\\^o": "ô", "\\^u": "û"
    }
    
    doc = Document(docx_path)
    
    def replace_in_runs(runs):
        for run in runs:
            if run.text: 
                texto = run.text
                for old, new in replacements.items():
                    if old in texto:
                        texto = texto.replace(old, new)
                run.text = texto

    for para in doc.paragraphs:
        replace_in_runs(para.runs)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_in_runs(para.runs)
                    
    doc.save(output_path)

def remove_repeating_headers_from_pdf(input_path: str, temp_path: str):
    """
    Elimina físicamente el área del encabezado de la página 2 en adelante.
    Conserva la página 1 intacta para mantener el diseño original.
    """
    doc = fitz.open(input_path)
    
    # Definimos un rectángulo de "censura" en la parte superior.
    # 130 es la altura en píxeles. Cubre el texto, el escudo y la línea verde.
    rect_encabezado = fitz.Rect(0, 0, doc[0].rect.width, 130)
    
    # Iteramos desde la segunda página (índice 1) hasta el final del PDF
    for page_num in range(1, len(doc)):
        page = doc[page_num]
        # Aplicamos la censura para borrar cualquier rastro de tinta/imágenes ahí
        page.add_redact_annot(rect_encabezado)
        page.apply_redactions()
        
    # Guardamos el PDF limpio
    doc.save(temp_path)
    doc.close()

def pdf_to_word(input_path: str, output_path: str) -> bool:
    """Convierte un archivo PDF a Word de forma directa y corrige el LaTeX."""
    try:
        # Conversión directa del PDF original (sin censura previa)
        cv = Converter(input_path)
        config = {
            "line_overlap": 0.8, 
            "word_margin": 2.5,  # Tolerancia alta para el texto justificado
            "line_margin": 0.1,
            "connected_border_tolerance": 2.0,
            "exact_margin_tolerance": 10,
        }
        cv.convert(output_path, start=0, end=None, **config)
        cv.close()
        
        # Corregir acentos de LaTeX
        fix_latex_accents_in_docx(output_path)
            
        return True
    except Exception as e:
        print(f"Error al convertir PDF a Word: {e}")
        return False

def pdf_to_excel(input_path: str, output_path: str) -> bool:
    """Pendiente de implementación con Camelot o pdfplumber"""
    pass

def pdf_to_powerpoint(input_path: str, output_path: str) -> bool:
    """Pendiente de implementación con python-pptx"""
    pass