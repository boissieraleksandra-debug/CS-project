import streamlit as st

def init():
    if "role" not in st.session_state:
        st.session_state.role = None

    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    if "saved" not in st.session_state:
        st.session_state.saved = []

    if "applications" not in st.session_state:
        st.session_state.applications = []

    if "student" not in st.session_state:
        st.session_state.student = {"name": ""}

    if "startup" not in st.session_state:
        st.session_state.startup = {"name": ""}


def create_task(title, desc, category):
    st.session_state.tasks.append({
        "id": len(st.session_state.tasks) + 1,
        "title": title,
        "description": desc,
        "category": category,
        "startup": st.session_state.startup["name"]
    })


def apply(task):
    st.session_state.applications.append({
        "task_id": task["id"],
        "task_title": task["title"],
        "startup": task["startup"],
        "student": st.session_state.student["name"],
        "status": "Applied",
        "details": "",
        "submission": ""
    })
