from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.normalize_service import normalize_text

router = APIRouter()


class NormalizeRequest(BaseModel):
    text: str


@router.post("/normalize")
async def normalize(req: NormalizeRequest):
    """
    Normaliza texto usando GPT (Opción A).
    """
    try:
        result = await normalize_text(req.text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:  # OPENAI_API_KEY missing or other config
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error interno normalizando el texto.",
        )


@router.post("/process")
async def process(req: NormalizeRequest):
    """
    Alias genérico /process para texto (la consigna lo pide).
    """
    return await normalize(req)
