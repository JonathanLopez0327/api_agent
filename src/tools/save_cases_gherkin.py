import json
import os
from typing import Any, Dict, List, Optional
from .case_store import get_cases


def _escape_table_cell(value: Any) -> str:
    s = str(value)
    return s.replace("|", "\\|")


def _case_to_gherkin_steps(case: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    cid = case.get("id", "")
    name = case.get("name", "")
    method = case.get("method", "")
    url = case.get("url", "")
    headers = case.get("headers", {}) or {}
    payload = case.get("payload", None)
    expected_status = case.get("expected_status", 200)
    notes = case.get("notes", "")

    if notes:
        lines.append(f"  # {notes}")
    # Omitir el identificador TC-XXX en el título del escenario según solicitud
    lines.append(f"  Scenario: {name}")
    lines.append("    Given preparo una solicitud HTTP")
    if headers:
        lines.append("    And los headers son:")
        lines.append("      | clave | valor |")
        for k, v in headers.items():
            lines.append(f"      | {k} | {_escape_table_cell(v)} |")
    if payload is not None:
        payload_str = json.dumps(payload, ensure_ascii=False, indent=2)
        lines.append("    And el payload es:")
        lines.append("      \"\"\"json")
        for pline in payload_str.splitlines():
            lines.append(f"      {pline}")
        lines.append("      \"\"\"")
    lines.append(f"    When envío una solicitud \"{method}\" a \"{url}\"")
    lines.append(f"    Then el código de estado debe ser {expected_status}")
    return lines


def cases_to_gherkin(cases: List[Dict[str, Any]], feature_name: str = "Casos de API") -> str:
    lines: List[str] = []
    lines.append("# language: en")
    lines.append(f"Feature: {feature_name}")
    lines.append("")
    for c in cases:
        lines.extend(_case_to_gherkin_steps(c))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def tool_save_cases_gherkin_by_id(
    cases_id: str,
    feature_path: Optional[str] = "api_test_cases.feature",
    feature_name: Optional[str] = "Casos de API",
    output_dir: Optional[str] = None,
) -> str:
    cases = get_cases(cases_id)
    if not cases:
        return f"No se encontraron casos para el id={cases_id}"
    content = cases_to_gherkin(cases, feature_name=feature_name or "Casos de API")
    # Si se especifica output_dir, escribir dentro del directorio usando el nombre base
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        feature_path = os.path.join(output_dir, os.path.basename(feature_path or "api_test_cases.feature"))
    # Asegurar directorio existente
    os.makedirs(os.path.dirname(feature_path) or ".", exist_ok=True)
    with open(feature_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Guardados {len(cases)} escenarios en {feature_path}"
