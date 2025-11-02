# API Agent – Generador de Casos de Prueba de API

Pequeño agente (LlamaIndex + Ollama) que genera casos de prueba de API (Happy Path + negativos), y los exporta a JSON, CSV y BDD Gherkin.

## Requisitos
- Python 3.10+ recomendado
- [Ollama](https://ollama.com) instalado y en ejecución (para usar un LLM local)
- Modelo Ollama disponible: el ejemplo usa `gpt-oss:20b`

## Instalación

Opción A – Mínima (recomendada):
- Instala solo lo que el código usa directamente.
```
python -m venv venv
# Windows (PowerShell)
.\\venv\\Scripts\\Activate.ps1
# macOS/Linux (bash)
# source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Opción B – Congelada (reproducible):
- Instala exactamente el entorno actual (más pesado, incluye `torch`, `transformers`, etc.).
```
pip install -r requirements.lock.txt
```

## Configurar el modelo (Ollama)
- Arranca Ollama y descarga el modelo del ejemplo:
```
ollama pull gpt-oss:20b
```
- Para cambiar el modelo, ajusta el parámetro `model` en `src/main.py:13`.

## Ejecución
- Ejecuta el agente de ejemplo, que genera casos y guarda los archivos de salida:
```
python src/main.py
```

## Salidas
Al ejecutarse, se crean por defecto en la raíz:
- `api_test_cases.json` – Lista de casos con `id`, `name`, `method`, `url`, `headers`, `payload`, `expected_status`, `notes`.
- `api_test_cases.csv` – Mismos campos en CSV (objetos serializados a JSON).
- `api_test_cases.feature` – Escenarios en formato BDD Gherkin (español).

También imprime métricas de tokens consumidos.

## ¿Cómo funciona?
- El agente usa herramientas (“tools”) para generar y guardar casos:
  - `tool_generate_cases_full(...)` genera casos y retorna un identificador en memoria. Ver firma en `src/tools/generate_cases.py:345`.
  - `tool_save_cases_by_id(cases_id, json_path, csv_path)` guarda JSON/CSV. Ver `src/tools/save_cases.py:23`.
  - `tool_save_cases_gherkin_by_id(cases_id, feature_path, feature_name)` guarda el `.feature`. Ver `src/tools/save_cases_gherkin.py:54`.
- `src/main.py` construye el `FunctionAgent` con estas tools y envía un prompt que orquesta el flujo.

## Personalización rápida
- Endpoint, método, headers, body, query y path: edita el bloque de `prompt` en `src/main.py`.
- Código de estado para negativos: cambia `negative_status` en el prompt o al llamar la tool.
- Mutaciones de headers: `mutate_headers=True` en la llamada a `tool_generate_cases_full` si quieres casos negativos de headers.
- Modelo LLM: cambia `model` en `src/main.py`.

## Uso directo de las tools (sin agente)
Ejemplo mínimo en un script Python:
```
from src.tools.generate_cases import tool_generate_cases_full
from src.tools.save_cases import tool_save_cases_by_id
from src.tools.save_cases_gherkin import tool_save_cases_gherkin_by_id

resp = tool_generate_cases_full(
    endpoint_template="https://api.mi-banco/transacciones/crear",
    method="POST",
    headers={"Content-Type": "application/json"},
    body={"monto": 123.45},
    query=None,
    path=None,
    base_case_name="POST - Happy Path",
    negative_status=400,
    mutate_headers=False,
)

cases_id = resp["cases_id"]
print("Total casos:", resp["total"])  # y algunos ejemplos en resp["examples"]

print(tool_save_cases_by_id(cases_id, json_path="api_test_cases.json", csv_path="api_test_cases.csv"))
print(tool_save_cases_gherkin_by_id(cases_id, feature_path="api_test_cases.feature", feature_name="Casos de API - BDD"))
```

## Problemas comunes
- “Modelo no encontrado”: ejecuta `ollama pull gpt-oss:20b` o cambia el nombre del modelo en `src/main.py`.
- “No se encontraron casos para el id=…“: asegúrate de usar el `cases_id` devuelto por `tool_generate_cases_full` al guardar.
- Errores al instalar el lock: algunos paquetes (e.g., `torch`) requieren compiladores o runtimes específicos; si no los necesitas, usa la opción mínima.

## Estructura relevante
- `src/main.py` – Configura LLM, agente y prompt de ejemplo.
- `src/tools/generate_cases.py` – Lógica de generación y tool de alto nivel.
- `src/tools/save_cases.py` – Guardado en JSON/CSV.
- `src/tools/save_cases_gherkin.py` – Exportación a BDD Gherkin.
- `src/tools/case_store.py` – Almacenamiento en memoria de casos (por `cases_id`).

¡Listo! Con esto puedes generar suites de pruebas API rápidamente y exportarlas en varios formatos.
