## Juan Magrini
# retoxmas2025-entregable-ia
Este proyecto implementa una API en **FastAPI** que integra:

- **Opción B – OCR con Tesseract**  
  - Endpoint principal: `POST /api/extract`
- **Opción A – Normalización de texto con GPT**  
  - Endpoint principal: `POST /api/normalize`

El objetivo es procesar páginas del padrón social del **Club Nacional de Football**:

1. Extraer el texto crudo a partir de una **imagen** (OCR).
2. Normalizar fragmentos de texto (por ejemplo, una fila de socio) a un formato estructurado usando un modelo de lenguaje.

---

## 1. Tecnologías utilizadas

- **Python 3.x**
- **FastAPI** – Framework para APIs REST.
- **Uvicorn** – ASGI server.
- **Tesseract OCR** – Motor de reconocimiento óptico de caracteres (instalado en el sistema).
- **pytesseract** – Wrapper de Tesseract para Python.
- **Pillow** – Manejo de imágenes.
- **OpenAI Python SDK** – Para llamar al modelo GPT (normalización).
- **Pydantic** – Validación de modelos de entrada/salida.

---

## 2. Estructura del proyecto

```bash
retoxmas2025-entregable-ia/
├─ app/
│  ├─ main.py                   # Crea la app FastAPI y monta los routers
│  ├─ routers/
│  │  ├─ __init__.py
│  │  ├─ ocr_router.py          # Endpoints de OCR (/api/extract, /api/process imagen)
│  │  └─ normalize_router.py    # Endpoints de normalización (/api/normalize, /api/process texto)
│  ├─ services/
│  │  ├─ __init__.py
│  │  ├─ ocr_service.py         # Lógica OCR con Tesseract
│  │  └─ normalize_service.py   # Lógica de llamado a GPT para normalizar
│  └─ __init__.py
├─ venv/                        # virtual env
├─ example/                     # Imágenes de ejemplo (páginas del padrón)
│  └─ pagina_socios.jpg
├─ requirements.txt
└─ README.md
```

## 3. Instalacion
- Crear y activar entorno virtual:
```bash
python -m venv venv
```
- 
```bash
venv\Scripts\activate
```
- Instalar dependencias
```bash
pip install -r requirements.txt
```

## 4. Tesseract OCR
Es necesario tener instalado Tesseract en el sitema operativo
- Ruta típica de windows: "C:\Program Files\Tesseract-OCR\tesseract.exe"


## 4.2 API Key de OpenAI
Para usar endpoints de normalización es necsario conffigurar una variable de entorno OPENAI_API_KEY
```bash
$env:OPENAI_API_KEY = "TU_API_KEY_DE_OPENAI_AQUI"
```

## 5. Ejecucion del servidor:
Desde la raíz del proyecto (con virtual env activado):
```bash
uvicorn app.main:app --reload
```


## 6. Endpoints
- OCR:
Endpoint principal de OCR. Recibe una imagen y devuelve el texto extraído.
- Content-Type: multipart/form-data
Parámetros:
- image: archivo de imagen (jpg, jpeg, png, tiff, bmp)

- Normalización:
POST /api/normalize
Normaliza un fragmento de texto que representa los datos de un socio.

- Content-Type: application/json

Body:

{
  "text": "LOPEZ CLAUDIO LARTIGAU, BV. ORDOÑEZ 1826 AP 20, Nac. 3/9/60, Ingr. 8/3/80"
}


El servicio envía el texto a GPT con un prompt que:
1. Separa nombre y apellidos.

2. Intenta normalizar fechas a YYYY-MM-DD.

3. Estandariza la dirección en un solo string.

4. Devuelve un JSON con metadatos de confianza.

Respuesta 200 (ejemplo):

```bash
{
  "nombre": "Claudio",
  "apellidos": "Lopez Lartigau",
  "direccion": "Bvar. Ordóñez 1826, apto 20",
  "fecha_nacimiento": "1960-09-03",
  "fecha_ingreso": "1980-03-08",
  "metadata": 
  {
    "confianza": "alta",
    "notas": "Fechas normalizadas al formato YYYY-MM-DD."
  }
}

```

## 7. Flujo típico de uso
1. OCR (imagen → texto)
- El usuario sube una foto escaneada de una página del padrón (/api/extract).
- La API responde con el texto crudo de toda la página.

2. Normalización (texto → JSON)
- Se toma una línea de ese texto (por ejemplo, los datos de un socio).
- Se envía al endpoint /api/normalize.
- La API responde con un JSON estructurado, listo para guardar en una base de datos o para análisis posterior.