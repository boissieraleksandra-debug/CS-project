"""
auth.py — tiny persistence helpers for the demo app's sign-in state.

We keep the current account in Streamlit query params and a tiny local file
so a browser refresh can rebuild st.session_state and the user stays signed in.

This is intentionally lightweight for a classroom/demo app:
    ?role=student&student_id=3
or  ?role=startup&startup_id=2
"""

import json
from pathlib import Path

import streamlit as st

from db import get_startup, get_student

AUTH_KEYS = (
    "role",
    "student_id",
    "startup_id",
)
LOGIN_STATE_PATH = Path(__file__).parent / ".login_state.json"


def _as_single(value):
    """Normalize Streamlit query-param values to a single string or None."""
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _load_saved_login():
    """Return persisted login info from disk, or None if missing/invalid."""
    if not LOGIN_STATE_PATH.exists():
        return None
    try:
        return json.loads(LOGIN_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _save_login(role: str, user_id: int):
    """Persist the active login to disk so refreshes can recover it."""
    payload = {"role": role, "user_id": user_id}
    LOGIN_STATE_PATH.write_text(json.dumps(payload), encoding="utf-8")


def _clear_saved_login():
    """Remove the on-disk login snapshot if it exists."""
    try:
        LOGIN_STATE_PATH.unlink()
    except FileNotFoundError:
        pass


def _apply_login(role: str, user_id: int):
    """Set session/query state for a validated account."""
    st.session_state["role"] = role
    st.query_params.clear()

    if role == "student":
        st.session_state["student_id"] = user_id
        st.session_state.pop("startup_id", None)
        st.query_params["role"] = "student"
        st.query_params["student_id"] = str(user_id)
    elif role == "startup":
        st.session_state["startup_id"] = user_id
        st.session_state.pop("student_id", None)
        st.query_params["role"] = "startup"
        st.query_params["startup_id"] = str(user_id)
    else:
        raise ValueError(f"Unsupported role: {role}")

    st.session_state.setdefault("mode", "view")


def _restore_role(role: str, user_id):
    """Validate and restore a role/id pair. Returns True on success."""
    try:
        resolved_id = int(user_id)
    except (TypeError, ValueError):
        return False

    if role == "student" and get_student(resolved_id):
        _apply_login("student", resolved_id)
        _save_login("student", resolved_id)
        return True

    if role == "startup" and get_startup(resolved_id):
        _apply_login("startup", resolved_id)
        _save_login("startup", resolved_id)
        return True

    return False


def restore_login():
    """Restore session state from query params if a valid account is present."""
    if st.session_state.get("role") == "student" and st.session_state.get("student_id"):
        return
    if st.session_state.get("role") == "startup" and st.session_state.get("startup_id"):
        return

    role = _as_single(st.query_params.get("role"))
    student_id = _as_single(st.query_params.get("student_id"))
    startup_id = _as_single(st.query_params.get("startup_id"))

    if role == "student" and student_id and _restore_role("student", student_id):
        return

    if role == "startup" and startup_id and _restore_role("startup", startup_id):
        return

    saved = _load_saved_login()
    if saved and _restore_role(saved.get("role"), saved.get("user_id")):
        return

    if role or student_id or startup_id or saved:
        clear_login()


def persist_login(role: str, user_id: int):
    """Persist the signed-in account to both session state and query params."""
    _apply_login(role, user_id)
    _save_login(role, user_id)


def clear_login():
    """Forget the current account from both session state and the URL."""
    for key in AUTH_KEYS:
        st.session_state.pop(key, None)
    st.query_params.clear()
    _clear_saved_login()
