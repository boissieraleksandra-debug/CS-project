import streamlit as st
from db import init_db, create_task

st.set_page_config(page_title="Post Task", page_icon="➕", layout="wide")
init_db()

if st.session_state.get("role") != "startup":
    st.stop()

st.title("➕ Post Task")

startup_name = st.session_state.get("startup_name", "")

title = st.text_input("Task Title")
category = st.text_input("Category")
location = st.text_input("Location")
duration = st.text_input("Duration")
budget = st.text_input("Budget")
remote_type = st.text_input("Remote Type")
description = st.text_area("Description")
skills_required = st.text_input("Skills Required")
deadline = st.text_input("Deadline")
task_details = st.text_area("Task Details")

if st.button("Post Task", use_container_width=True):
    create_task(
        title,
        startup_name,
        category,
        location,
        duration,
        budget,
        remote_type,
        description,
        skills_required,
        deadline,
        task_details
    )
    st.success("Task posted")
