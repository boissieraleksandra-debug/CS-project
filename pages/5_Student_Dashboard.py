import streamlit as st
from db import init_db, get_applications_for_student, get_saved_task_ids

st.set_page_config(page_title="Student Dashboard", page_icon="📊", layout="wide")
init_db()

if st.session_state.get("role") != "student":
    st.warning("Please go to the home page and choose Student first.")
    st.stop()

student_name = st.session_state.get("student_name", "")
apps = get_applications_for_student(student_name)
saved_ids = get_saved_task_ids()

st.title("📊 Student Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Saved Tasks", len(saved_ids))
col2.metric("Applications", len(apps))
col3.metric("Completed", sum(1 for a in apps if a["status"] == "Completed"))

st.subheader("Task Status Overview")
for app in apps:
    st.write(f"- {app['task_title']}: {app['status']}")
