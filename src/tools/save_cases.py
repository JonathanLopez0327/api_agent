# tools/save_cases.py
import json
import csv
import os
from typing import Any, Dict, List, Optional
from .case_store import get_cases

def save_cases_to_files(
    cases: List[Dict[str, Any]],
    json_path: str = "api_test_cases.json",
    csv_path: str = "api_test_cases.csv",
) -> None:
    # Asegurar directorios de destino
    os.makedirs(os.path.dirname(json_path) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(csv_path) or ".", exist_ok=True)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)

    fieldnames = ["id", "name", "method", "url", "headers", "payload", "expected_status", "notes"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for c in cases:
            row = dict(c)
            if isinstance(row.get("headers"), (dict, list)):
                row["headers"] = json.dumps(row["headers"], ensure_ascii=False)
            if isinstance(row.get("payload"), (dict, list)):
                row["payload"] = json.dumps(row["payload"], ensure_ascii=False)
            writer.writerow(row)

def tool_save_cases_by_id(
    cases_id: str,
    json_path: Optional[str] = "api_test_cases.json",
    csv_path: Optional[str] = "api_test_cases.csv",
    output_dir: Optional[str] = None,
) -> str:
    cases = get_cases(cases_id)
    if not cases:
        return f"No se encontraron casos para el id={cases_id}"
    # Si se especifica output_dir, forzar los archivos dentro de ese directorio
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        if json_path:
            json_path = os.path.join(output_dir, os.path.basename(json_path))
        if csv_path:
            csv_path = os.path.join(output_dir, os.path.basename(csv_path))
    save_cases_to_files(cases, json_path=json_path or "api_test_cases.json", csv_path=csv_path or "api_test_cases.csv")
    return f"Guardados {len(cases)} casos en {json_path} y {csv_path}"
