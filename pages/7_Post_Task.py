import streamlit as st
from db import init_db, get_startup_profile, create_task
from ui import apply_styles, header

st.set_page_config(page_title="Post Task", page_icon="➕", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "startup":
    st.stop()

profile = get_startup_profile()

header("➕ Post a Task", "Create a task that students will see in their discovery feed.")

if not profile["startup_name"]:
    st.warning("Please save your startup profile first.")
    st.stop()

title = st.text_input("Task Title")
category = st.selectbox("Category", ["Marketing", "Design", "Product", "Operations", "Strategy", "Research", "Tech"])
location = st.text_input("Location")
duration = st.text_input("Duration")
budget = st.text_input("Budget")
remote_type = st.selectbox("Remote Type", ["Remote", "Hybrid", "On-site"])
description = st.text_area("Short Description")
skills_required = st.text_input("Required Skills")
deadline = st.text_input("Application Deadline")
task_details = st.text_area("Initial Task Details")

if st.button("Post Task", use_container_width=True):
    create_task({
        "title": title,
        "startup_name": profile["startup_name"],
        "category": category,
        "location": location,
        "duration": duration,
        "budget": budget,
        "remote_type": remote_type,
        "description": description,
        "skills_required": skills_required,
        "deadline": deadline,
        "task_details": task_details,
        "status": "Open",
    })
    st.success("Task posted successfully.")
