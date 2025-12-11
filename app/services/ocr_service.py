# app/services/ocr_service.py
import io
from fastapi import UploadFile
from PIL import Image
import pytesseract

import io
from fastapi import UploadFile
from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


async def extract_text_from_image(image: UploadFile) -> str:
    contents = await image.read()

    try:
        pil_image = Image.open(io.BytesIO(contents))
    except Exception:
        raise ValueError("No se pudo abrir la imagen. Verificar el archivo enviado.")

    # Escala de grises
    pil_image = pil_image.convert("L")

    # Página con muchas columnas -> bloque de texto uniforme
    custom_config = r"--psm 6"

    text = pytesseract.image_to_string(
        pil_image,
        config=custom_config,
    )

    return text.strip()
