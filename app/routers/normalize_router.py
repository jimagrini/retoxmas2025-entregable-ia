# app/routers/normalize_router.py
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
    except RuntimeError as e:  # falta OPENAI_API_KEY u otra config
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # 👇 mientras desarrollamos, mostramos el error real
        raise HTTPException(
            status_code=500,
            detail=f"Error interno normalizando el texto: {repr(e)}",
        )


@router.post("/process")
async def process(req: NormalizeRequest):
    """
    Alias genérico /process para texto (misma lógica que /normalize).
    """
    return await normalize(req)
