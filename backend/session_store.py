from typing import Dict, List, Any

# In-memory store: { session_id: [grant, ...] }
_grants: Dict[str, List[Dict[str, Any]]] = {}


def save_grants(session_id: str, grants: List[Dict[str, Any]]):
    _grants[session_id] = grants


def get_grants(session_id: str) -> List[Dict[str, Any]]:
    return _grants.get(session_id, [])
