"""
In-memory session store for Scout.
Tracks grants, chat history, and shared context between agents.
"""
from typing import Dict, List, Any, Optional

# In-memory stores
_grants: Dict[str, List[Dict[str, Any]]] = {}
_messages: Dict[str, List[Dict[str, Any]]] = {}
_workspace: Dict[str, Dict[str, Any]] = {}


# --- Grant Storage ---

def save_grants(session_id: str, grants: List[Dict[str, Any]]):
    _grants[session_id] = grants


def get_grants(session_id: str) -> List[Dict[str, Any]]:
    return _grants.get(session_id, [])


# --- Chat History ---

def append_message(session_id: str, role: str, content: str, agent: str = "system"):
    if session_id not in _messages:
        _messages[session_id] = []
    _messages[session_id].append({
        "role": role,
        "content": content,
        "agent": agent,
    })


def get_messages(session_id: str) -> List[Dict[str, Any]]:
    return _messages.get(session_id, [])


# --- Shared Workspace (inter-agent context) ---

def set_workspace(session_id: str, key: str, value: Any):
    """Store a value in the session workspace so downstream agents can access it."""
    if session_id not in _workspace:
        _workspace[session_id] = {}
    _workspace[session_id][key] = value


def get_workspace(session_id: str, key: str, default: Any = None) -> Any:
    return _workspace.get(session_id, {}).get(key, default)


def get_full_workspace(session_id: str) -> Dict[str, Any]:
    return _workspace.get(session_id, {})
