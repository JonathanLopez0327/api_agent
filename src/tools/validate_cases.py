import os
import time
from typing import Any, Dict, List, Optional, Tuple

import requests

from .case_store import get_cases


def _load_token_headers() -> Dict[str, str]:
    token = os.getenv("API_TOKEN") or os.getenv("BEARER_TOKEN")
    if not token:
        return {}
    header_name = os.getenv("API_AUTH_HEADER", "Authorization")
    value = token if token.lower().startswith("bearer ") else f"Bearer {token}"
    return {header_name: value}


def _merge_headers(*headers_list: Optional[Dict[str, Any]]) -> Dict[str, str]:
    merged: Dict[str, str] = {}
    for h in headers_list:
        if not h:
            continue
        for k, v in h.items():
            merged[str(k)] = str(v)
    return merged


def _send_request(method: str, url: str, headers: Dict[str, str], payload: Optional[Any], timeout: float) -> Tuple[int, float, Optional[Any], Optional[str]]:
    start = time.perf_counter()
    try:
        resp = requests.request(method=method.upper(), url=url, headers=headers, json=payload, timeout=timeout)
        elapsed = (time.perf_counter() - start) * 1000.0
        content_type = resp.headers.get("Content-Type", "")
        body_json: Optional[Any] = None
        body_text: Optional[str] = None
        if "application/json" in content_type.lower():
            try:
                body_json = resp.json()
            except Exception:
                body_text = resp.text[:500]
        else:
            body_text = resp.text[:500]
        return resp.status_code, elapsed, body_json, body_text
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000.0
        return -1, elapsed, None, f"{type(e).__name__}: {e}"


def tool_validate_cases_by_id(
    cases_id: str,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    """
    Envía las solicitudes definidas en los casos y valida el status esperado.
    Lee el token del entorno (.env):
      - API_TOKEN (o BEARER_TOKEN)
      - API_AUTH_HEADER (por defecto 'Authorization')
    """
    cases = get_cases(cases_id)
    if not cases:
        return {"error": f"No se encontraron casos para el id={cases_id}"}

    token_headers = _load_token_headers()
    results: List[Dict[str, Any]] = []
    passed = 0

    for c in cases:
        method = str(c.get("method", "GET")).upper()
        url = str(c.get("url", ""))
        payload = c.get("payload")
        expected_status = int(c.get("expected_status", 200))
        case_headers = c.get("headers", {}) or {}

        headers = _merge_headers(case_headers, token_headers)

        status, rt_ms, body_json, body_text_or_err = _send_request(method, url, headers, payload, timeout)

        ok = (status == expected_status)
        if ok:
            passed += 1

        results.append({
            "id": c.get("id"),
            "name": c.get("name"),
            "method": method,
            "url": url,
            "expected": expected_status,
            "actual": status,
            "ok": ok,
            "response_time_ms": round(rt_ms, 2),
            "response_json": body_json if ok else None,
            "response_excerpt": None if ok else (body_text_or_err if body_json is None else None),
            "error": None if status >= 0 else body_text_or_err,
        })

    summary = {
        "cases_id": cases_id,
        "total": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
    }

    return {"summary": summary, "results": results[:10]}  # limitar salida

