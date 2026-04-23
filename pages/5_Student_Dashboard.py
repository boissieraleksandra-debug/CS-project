import streamlit as st
import pandas as pd
import plotly.express as px
from db import init_db, get_student_profile, get_applications_for_student, get_saved_task_ids, get_all_tasks
from ui import apply_styles, header

st.set_page_config(page_title="Student Dashboard", page_icon="📊", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "student":
    st.stop()

profile = get_student_profile()
student_name = profile["full_name"]

header("📊 Student Dashboard", "See your task activity, pipeline, and strongest categories.")

saved_ids = get_saved_task_ids()
all_tasks = get_all_tasks()
saved_tasks = [t for t in all_tasks if t["id"] in saved_ids]
applications = get_applications_for_student(student_name) if student_name else []

completed_count = sum(1 for a in applications if a["status"] == "Completed")
matched_count = sum(1 for a in applications if a["status"] == "Matched")

c1, c2, c3 = st.columns(3)
c1.metric("Saved Tasks", len(saved_tasks))
c2.metric("Applications", len(applications))
c3.metric("Completed", completed_count)

if saved_tasks or applications:
    category_counts = {}
    for task in saved_tasks:
        category_counts[task["category"]] = category_counts.get(task["category"], 0) + 1

    task_lookup = {t["id"]: t for t in all_tasks}
    for app in applications:
        task = task_lookup.get(app["task_id"])
        if task:
            category_counts[task["category"]] = category_counts.get(task["category"], 0) + 1

    df = pd.DataFrame({
        "Category": list(category_counts.keys()),
        "Count": list(category_counts.values())
    })

    fig = px.bar(df, x="Category", y="Count", color="Category", text="Count")
    fig.update_layout(showlegend=False)
    st.subheader("Your Activity by Category")
    st.plotly_chart(fig, use_container_width=True)

status_counts = {}
for app in applications:
    status_counts[app["status"]] = status_counts.get(app["status"], 0) + 1

if status_counts:
    df2 = pd.DataFrame({
        "Status": list(status_counts.keys()),
        "Count": list(status_counts.values())
    })
    fig2 = px.pie(df2, names="Status", values="Count", hole=0.55)
    st.subheader("Application Status Breakdown")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Apply to tasks to generate dashboard insights.")
