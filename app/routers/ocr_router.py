from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ocr_service import extract_text_from_image
from pytesseract import TesseractNotFoundError

router = APIRouter()

@router.post("/extract")
async def extract(image: UploadFile = File(...)):
    """
    Extrae text from an image using Tesseract.
    """
    try:
        text = await extract_text_from_image(image)
        return {
            "filename": image.filename,
            "text": text
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TesseractNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Tesseract not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {repr(e)}")



@router.post("/process")
async def process(image: UploadFile = File(...)):

    return await extract(image)
