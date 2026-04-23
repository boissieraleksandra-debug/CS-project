import streamlit as st
import pandas as pd
import plotly.express as px
from db import init_db, get_startup_profile, get_startup_tasks, get_applications_for_startup
from ui import apply_styles, header

st.set_page_config(page_title="Startup Dashboard", page_icon="📈", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "startup":
    st.stop()

profile = get_startup_profile()
startup_name = profile["startup_name"]

header("📈 Startup Dashboard", "Track tasks, applicants, and hiring pipeline performance.")

if not startup_name:
    st.warning("Please save your startup profile first.")
    st.stop()

tasks = get_startup_tasks(startup_name)
applications = get_applications_for_startup(startup_name)

matched_count = sum(1 for a in applications if a["status"] == "Matched")
completed_count = sum(1 for a in applications if a["status"] == "Completed")

c1, c2, c3 = st.columns(3)
c1.metric("Posted Tasks", len(tasks))
c2.metric("Applications", len(applications))
c3.metric("Completed Tasks", completed_count)

if tasks:
    category_counts = {}
    for task in tasks:
        category_counts[task["category"]] = category_counts.get(task["category"], 0) + 1

    df = pd.DataFrame({
        "Category": list(category_counts.keys()),
        "Tasks": list(category_counts.values())
    })
    fig = px.bar(df, x="Category", y="Tasks", color="Category", text="Tasks")
    fig.update_layout(showlegend=False)
    st.subheader("Tasks by Category")
    st.plotly_chart(fig, use_container_width=True)

if applications:
    status_counts = {}
    for app in applications:
        status_counts[app["status"]] = status_counts.get(app["status"], 0) + 1

    df2 = pd.DataFrame({
        "Status": list(status_counts.keys()),
        "Count": list(status_counts.values())
    })
    fig2 = px.pie(df2, names="Status", values="Count", hole=0.55)
    st.subheader("Application Status Breakdown")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No application data yet.")
