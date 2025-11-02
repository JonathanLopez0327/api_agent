# tools/save_cases.py
import json
import csv
from typing import Any, Dict, List, Optional
from .case_store import get_cases

def save_cases_to_files(cases: List[Dict[str, Any]], json_path="api_test_cases.json", csv_path="api_test_cases.csv"):
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
) -> str:
    cases = get_cases(cases_id)
    if not cases:
        return f"No se encontraron casos para el id={cases_id}"
    save_cases_to_files(cases, json_path=json_path, csv_path=csv_path)
    return f"Guardados {len(cases)} casos en {json_path} y {csv_path}"
