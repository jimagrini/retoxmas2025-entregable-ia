from typing import Any, Dict
import os
import json

from openai import OpenAI

SYSTEM_PROMPT = """
Eres un servicio que normaliza registros del padrón social del Club Nacional de Football.

Te enviaré un fragmento de texto con los datos de una persona en formato libre
(puede venir de OCR, tener abreviaturas o errores).

Debes:
- Separar nombre y apellido.
- Normalizar fechas al formato YYYY-MM-DD.
  - Si falta el día, usar "01".
  - Si faltan día y mes, usar "01-01".
- Estandarizar la dirección en un solo string.
- Si un dato no puede inferirse con suficiente certeza, usar null.

Responde SIEMPRE en JSON válido con exactamente esta estructura:

{
  "nombre": "string o null",
  "apellidos": "string o null",
  "direccion": "string o null",
  "fecha_nacimiento": "YYYY-MM-DD o null",
  "fecha_ingreso": "YYYY-MM-DD o null",
  "metadata": {
    "confianza": "alta | media | baja",
    "notas": "texto breve explicando supuestos importantes"
  }
}

No incluyas nada fuera del JSON.
"""


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY no está configurada.")
    return OpenAI(api_key=api_key)


async def normalize_text(raw_text: str) -> Dict[str, Any]:
    """
    Llama a GPT para normalizar el texto y devuelve un dict con la estructura definida.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("El campo 'text' no puede estar vacío.")

    client = get_client()

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        response_format={"type": "json_object"},
    )

    json_str = response.output_text

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return {
            "nombre": None,
            "apellidos": None,
            "direccion": None,
            "fecha_nacimiento": None,
            "fecha_ingreso": None,
            "metadata": {
                "confianza": "baja",
                "notas": "No se pudo parsear el JSON devuelto por el modelo.",
                "raw_output": json_str,
            },
        }

    return data
