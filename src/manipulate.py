# src/manipulate.py
from pypdf import PdfReader, PdfWriter
import os

def merge_pdfs(pdf_paths: list, output_path: str) -> bool:
    """Une múltiples PDFs en uno solo."""
    try:
        writer = PdfWriter()
        for path in pdf_paths:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
        
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
        return True
    except Exception as e:
        print(f"Error al unir PDFs: {e}")
        return False

def split_pdf(input_path: str, output_folder: str) -> bool:
    """Separa un PDF, creando un archivo nuevo por cada página."""
    try:
        reader = PdfReader(input_path)
        base_name = os.path.basename(input_path).replace(".pdf", "")
        
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            
            output_path = os.path.join(output_folder, f"{base_name}_pag_{i+1}.pdf")
            with open(output_path, "wb") as f_out:
                writer.write(f_out)
        return True
    except Exception as e:
        print(f"Error al separar PDF: {e}")
        return False

def remove_page(input_path: str, page_index_to_remove: int, output_path: str) -> bool:
    """Elimina una página específica (el índice empieza en 0)."""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for i, page in enumerate(reader.pages):
            if i != page_index_to_remove:
                writer.add_page(page)
                
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
        return True
    except Exception as e:
        print(f"Error al eliminar página: {e}")
        return False