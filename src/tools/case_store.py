# tools/case_store.py
import uuid
from typing import Dict, List, Any

_CASES: Dict[str, List[Dict[str, Any]]] = {}

def put_cases(cases: List[Dict[str, Any]]) -> str:
    key = str(uuid.uuid4())
    _CASES[key] = cases
    return key

def get_cases(key: str) -> List[Dict[str, Any]]:
    return _CASES.get(key, [])
