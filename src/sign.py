# src/sign.py
from pyhanko.sign import signers
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.pdf_utils.writer import copy_into_new_writer

def sign_pdf(input_path: str, output_path: str, p12_path: str, p12_password: str) -> bool:
    """Añade una firma digital invisible estándar PAdES al PDF."""
    try:
        # Cargar el certificado digital (archivo .p12 o .pfx)
        signer = signers.SimpleSigner.load_pkcs12(
            pfx_file=p12_path,
            b_password=p12_password.encode('utf-8')
        )
        
        # Leer el PDF original y preparar el nuevo
        with open(input_path, 'rb') as f_in:
            reader = PdfFileReader(f_in)
            writer = copy_into_new_writer(reader)
            
            # Realizar la firma
            with open(output_path, 'wb') as f_out:
                signers.sign_pdf(
                    writer, 
                    signers.PdfSignatureMetadata(field_name='FirmaApp'),
                    signer=signer,
                    in_place=False,
                    out_dir=None,
                    existing_fields_only=False,
                    bytes_reserved=8192,
                    output=f_out
                )
        return True
    except Exception as e:
        print(f"Error al firmar PDF: {e}")
        return False