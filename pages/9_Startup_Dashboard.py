import streamlit as st
from db import init_db, get_tasks_for_startup, get_applications_for_startup

st.set_page_config(page_title="Startup Dashboard", page_icon="📈", layout="wide")
init_db()

if st.session_state.get("role") != "startup":
    st.warning("Please go to the home page and choose Startup first.")
    st.stop()

startup_name = st.session_state.get("startup_name", "")

st.title("📈 Startup Dashboard")

if not startup_name:
    st.info("Please save your startup profile first.")
    st.stop()

tasks = get_tasks_for_startup(startup_name)
apps = get_applications_for_startup(startup_name)

col1, col2, col3 = st.columns(3)
col1.metric("Posted Tasks", len(tasks))
col2.metric("Applications", len(apps))
col3.metric("Completed", sum(1 for a in apps if a["status"] == "Completed"))

st.subheader("Task Overview")
for task in tasks:
    st.write(f"- {task['title']} ({task['status']})")
