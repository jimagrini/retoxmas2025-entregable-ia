from fastapi import FastAPI
from app.routers.ocr_router import router as ocr_router
from app.routers.normalize_router import router as normalize_router
app = FastAPI(
    title="OCR Service - Proyecto IA",
    version="1.0.0",
    description="Servicio de extracción de texto desde imágenes usando Tesseract (Opción B)."
)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# OCR Router
app.include_router(ocr_router, prefix="/api", tags=["ocr"])

# Normalize Router
app.include_router(normalize_router, prefix="/api", tags=["normalize"])