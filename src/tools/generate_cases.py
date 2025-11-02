# generate_cases.py
# Lógica pura de generación de casos de prueba de API
# - Soporta: GET (query + path), POST/PUT/PATCH (body), DELETE/HEAD/OPTIONS
# - Siempre recibe headers
# - Genera: Happy Path + mutaciones negativas sobre body/query (y opcionalmente headers)

import copy
from typing import Any, Dict, List, Tuple, Union, Optional
from urllib.parse import urlencode
from .case_store import put_cases

# =========================
# Tipos
# =========================
Json = Dict[str, Any]
Path = Tuple[Union[str, int], ...]

# =========================
# Constantes
# =========================
_METHODS_WITHOUT_BODY_BY_DEFAULT = {"GET", "DELETE", "HEAD", "OPTIONS"}
_PROTECTED_HEADERS = {"authorization", "x-api-key"}  # ajusta según tu realidad

# =========================
# Utils para recorrer/mutar estructuras
# =========================
def _flatten_paths(obj: Any, base: Path = ()) -> List[Tuple[Path, Any]]:
    """Devuelve [(path_tuple, value), ...] para cada hoja del JSON."""
    paths: List[Tuple[Path, Any]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            paths.extend(_flatten_paths(v, base + (k,)))
    elif isinstance(obj, list):
        for idx, v in enumerate(obj):
            paths.extend(_flatten_paths(v, base + (idx,)))
    else:
        paths.append((base, obj))
    return paths

def _set_in(obj: Any, path: Path, new_value: Any) -> Any:
    cur = obj
    for p in path[:-1]:
        cur = cur[p]
    cur[path[-1]] = new_value
    return obj

def _del_in(obj: Any, path: Path) -> Any:
    cur = obj
    for p in path[:-1]:
        cur = cur[p]
    del cur[path[-1]]
    return obj

def _path_to_str(path: Path) -> str:
    return ".".join(str(p) for p in path)

# =========================
# Mutaciones por defecto (inyectable)
# =========================
def _default_mutations(value: Any, negative_status: int) -> List[Tuple[str, Any, int, str]]:
    """[(nombre_mutación, nuevo_valor, expected_status, nota), ...]"""
    muts: List[Tuple[str, Any, int, str]] = []
    muts.append(("Set null", None, negative_status, "Campo en null"))

    v = value
    if isinstance(v, bool):
        muts.append(("Wrong type (bool->str)", "true" if v else "false", negative_status, "Tipo incorrecto"))
        muts.append(("Wrong type (bool->int)", 1 if v else 0, negative_status, "Tipo incorrecto"))
    elif isinstance(v, (int, float)):
        muts.append(("Wrong type (num->str)", str(v), negative_status, "Tipo incorrecto"))
        muts.append(("Out of range (negative)", -abs(v) - 1, negative_status, "Valor fuera de rango"))
        muts.append(("Out of range (huge)", 10**12, negative_status, "Valor fuera de rango"))
    elif isinstance(v, str):
        muts.append(("Empty string", "", negative_status, "String vacío"))
        muts.append(("Too long string", v + ("X" * 256), negative_status, "String demasiado largo"))
        muts.append(("Wrong type (str->int)", 123, negative_status, "Tipo incorrecto"))
    elif isinstance(v, list):
        muts.append(("Empty list", [], negative_status, "Lista vacía"))
        muts.append(("Wrong type (list->str)", "[]", negative_status, "Tipo incorrecto"))
    elif isinstance(v, dict):
        muts.append(("Empty object", {}, negative_status, "Objeto vacío"))
        muts.append(("Wrong type (obj->str)", "{}", negative_status, "Tipo incorrecto"))
    elif v is None:
        muts.append(("None->str)", "null", negative_status, "Tipo incorrecto"))
        muts.append(("None->int)", 0, negative_status, "Tipo incorrecto"))
    else:
        muts.append(("Unknown type->str", "INVALID", negative_status, "Tipo incorrecto"))
    return muts

# =========================
# URL helpers (path params + query)
# =========================
def _apply_path_params(endpoint_template: str, path_params: Optional[Json]) -> str:
    """Reemplaza {param} con valores de path_params en el endpoint_template."""
    if not path_params:
        return endpoint_template
    url = endpoint_template
    for k, v in path_params.items():
        url = url.replace("{" + str(k) + "}", str(v))
    return url

def _compose_url(endpoint_template: str, path_params: Optional[Json], query_params: Optional[Json]) -> str:
    base = _apply_path_params(endpoint_template, path_params)
    if query_params and len(query_params) > 0:
        return f"{base}?{urlencode(query_params, doseq=True)}"
    return base

# =========================
# Creadores de casos
# =========================
def _create_base_case(
    request_body: Optional[Json],
    endpoint_url: str,
    method: str,
    headers: Json,
    base_case_name: str
) -> Dict[str, Any]:
    return {
        "id": "TC-001",
        "name": base_case_name,
        "method": method,
        "url": endpoint_url,
        "headers": copy.deepcopy(headers),
        "payload": copy.deepcopy(request_body) if request_body is not None else None,
        "expected_status": 200,
        "notes": "Caso feliz con request tal cual."
    }

def _create_test_case(
    tc_id: int,
    name: str,
    method: str,
    endpoint_url: str,
    headers: Json,
    payload: Optional[Json],
    status: int,
    notes: str
) -> Dict[str, Any]:
    return {
        "id": f"TC-{tc_id:03d}",
        "name": name,
        "method": method,
        "url": endpoint_url,
        "headers": copy.deepcopy(headers),
        "payload": copy.deepcopy(payload) if payload is not None else None,
        "expected_status": status,
        "notes": notes
    }

# =========================
# Helpers internos (tu orquestación reducida)
# =========================
def _normalize_inputs(
    method: str,
    headers: Optional[Json],
    body: Optional[Json],
    query: Optional[Json]
) -> Tuple[str, Json, Optional[Json], Json]:
    method = method.upper()
    headers = headers or {"Content-Type": "application/json"}
    query = copy.deepcopy(query) if query else {}
    if body is not None:
        body = copy.deepcopy(body)
    else:
        body = None if method in _METHODS_WITHOUT_BODY_BY_DEFAULT else {}
    return method, headers, body, query

def _gen_body_cases(
    *,
    cases: List[Dict[str, Any]],
    body: Optional[Json],
    base_url: str,
    method: str,
    headers: Json,
    negative_status: int,
    mutation_fn
) -> int:
    tc_counter = 2 if not cases else int(cases[-1]["id"].split("-")[-1]) + 1
    if body in (None, {}):
        return tc_counter

    for path_tuple, value in _flatten_paths(body):
        if isinstance(path_tuple[-1], str):
            try:
                variant = copy.deepcopy(body)
                _del_in(variant, path_tuple)
                cases.append(_create_test_case(
                    tc_counter,
                    f"[BODY] Missing field: {_path_to_str(path_tuple)}",
                    method, base_url, headers, variant,
                    negative_status,
                    f"Se elimina el campo {_path_to_str(path_tuple)} del body"
                ))
                tc_counter += 1
            except Exception:
                pass

        for mut_name, new_val, status, note in mutation_fn(value, negative_status):
            try:
                variant = copy.deepcopy(body)
                _set_in(variant, path_tuple, new_val)
                cases.append(_create_test_case(
                    tc_counter,
                    f"[BODY] {mut_name}: {_path_to_str(path_tuple)}",
                    method, base_url, headers, variant, status, note
                ))
                tc_counter += 1
            except Exception:
                continue
    return tc_counter

def _gen_query_cases(
    *,
    cases: List[Dict[str, Any]],
    endpoint_template: str,
    path: Optional[Json],
    query: Json,
    base_url: str,
    method: str,
    headers: Json,
    body: Optional[Json],
    negative_status: int,
    mutation_fn
) -> int:
    tc_counter = 2 if not cases else int(cases[-1]["id"].split("-")[-1]) + 1
    if not query:
        return tc_counter

    for path_tuple, value in _flatten_paths(query):
        if isinstance(path_tuple[-1], str):
            try:
                vq = copy.deepcopy(query)
                _del_in(vq, path_tuple)
                urlv = _compose_url(endpoint_template, path, vq)
                cases.append(_create_test_case(
                    tc_counter,
                    f"[QUERY] Missing param: {_path_to_str(path_tuple)}",
                    method, urlv, headers, body,
                    negative_status,
                    f"Se elimina el parámetro de query {_path_to_str(path_tuple)}"
                ))
                tc_counter += 1
            except Exception:
                pass

        for mut_name, new_val, status, note in mutation_fn(value, negative_status):
            try:
                vq = copy.deepcopy(query)
                _set_in(vq, path_tuple, new_val)
                urlv = _compose_url(endpoint_template, path, vq)
                cases.append(_create_test_case(
                    tc_counter,
                    f"[QUERY] {mut_name}: {_path_to_str(path_tuple)}",
                    method, urlv, headers, body, status, note
                ))
                tc_counter += 1
            except Exception:
                continue
    return tc_counter

def _gen_header_cases(
    *,
    cases: List[Dict[str, Any]],
    base_url: str,
    method: str,
    headers: Json,
    body: Optional[Json],
    negative_status: int,
    mutate_headers: bool
) -> int:
    tc_counter = 2 if not cases else int(cases[-1]["id"].split("-")[-1]) + 1
    if not mutate_headers or not headers:
        return tc_counter

    for k, v in list(headers.items()):
        if str(k).lower() in _PROTECTED_HEADERS:
            continue

        vh = copy.deepcopy(headers)
        vh.pop(k, None)
        cases.append(_create_test_case(
            tc_counter,
            f"[HEADERS] Missing header: {k}",
            method, base_url, vh, body, negative_status, f"Se elimina el header {k}"
        ))
        tc_counter += 1

        for name, new_val, status, note in [
            (f"[HEADERS] Empty value: {k}", "", negative_status, "Header vacío"),
            (f"[HEADERS] Wrong type (to int): {k}", 123, negative_status, "Tipo incorrecto (no string)"),
            (f"[HEADERS] Too long value: {k}", str(v) + ("X" * 256), negative_status, "Valor demasiado largo"),
        ]:
            vh = copy.deepcopy(headers)
            vh[k] = new_val
            cases.append(_create_test_case(tc_counter, name, method, base_url, vh, body, status, note))
            tc_counter += 1

    return tc_counter

# =========================
# Orquestador minimalista
# =========================
def generate_api_test_cases(
    *,
    endpoint_template: str,
    method: str = "POST",
    headers: Optional[Json] = None,
    body: Optional[Json] = None,
    query: Optional[Json] = None,
    path: Optional[Json] = None,
    base_case_name: str = "Base - Happy Path",
    negative_status: int = 400,
    mutate_headers: bool = False,
    mutation_fn = _default_mutations,
) -> List[Dict[str, Any]]:
    """Prepara entradas, crea el caso base y delega en helpers."""
    method, headers, body, query = _normalize_inputs(method, headers, body, query)
    base_url = _compose_url(endpoint_template, path, query)

    cases: List[Dict[str, Any]] = [
        _create_base_case(body, base_url, method, headers, base_case_name)
    ]

    _gen_body_cases(
        cases=cases, body=body, base_url=base_url, method=method,
        headers=headers, negative_status=negative_status, mutation_fn=mutation_fn
    )

    _gen_query_cases(
        cases=cases, endpoint_template=endpoint_template, path=path,
        query=query, base_url=base_url, method=method, headers=headers, body=body,
        negative_status=negative_status, mutation_fn=mutation_fn
    )

    _gen_header_cases(
        cases=cases, base_url=base_url, method=method, headers=headers, body=body,
        negative_status=negative_status, mutate_headers=mutate_headers
    )

    return cases

# =========================
# Wrapper "tool" completo (opcional)
# =========================
def tool_generate_cases_full(
    *,
    endpoint_template: str,
    method: str = "POST",
    headers: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    query: Optional[Dict[str, Any]] = None,
    path: Optional[Dict[str, Any]] = None,
    base_case_name: str = "Base - Happy Path",
    negative_status: int = 400,
    mutate_headers: bool = False,
) -> Dict[str, Any]:
    """
    Genera casos y los GUARDA en memoria. Devuelve un dict pequeño:
      {'cases_id': str, 'total': int, 'examples': [str, str, str]}
    """
    cases: List[Dict[str, Any]] = generate_api_test_cases(
        endpoint_template=endpoint_template,
        method=method,
        headers=headers,
        body=body,
        query=query,
        path=path,
        base_case_name=base_case_name,
        negative_status=negative_status,
        mutate_headers=mutate_headers,
    )
    cases_id = put_cases(cases)
    examples = [c["name"] for c in cases[:3]]  # primeros 3 nombres
    return {"cases_id": cases_id, "total": len(cases), "examples": examples}

