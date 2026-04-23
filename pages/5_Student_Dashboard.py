import streamlit as st
import pandas as pd
import plotly.express as px
from app_data import initialize_state
from ui import apply_global_styles, page_header

st.set_page_config(page_title="Student Dashboard", page_icon="📊", layout="wide")

initialize_state()
apply_global_styles()
page_header("📊 Student Dashboard", "Your activity, task pipeline, and strongest task categories in one place.")

saved_count = len(st.session_state.saved_tasks)
applied_count = len(st.session_state.applied_tasks)
completed_count = sum(1 for task in st.session_state.applied_tasks if task.get("status") == "Completed")

col1, col2, col3 = st.columns(3)
col1.metric("Saved Tasks", saved_count)
col2.metric("Applications Sent", applied_count)
col3.metric("Completed Tasks", completed_count)

all_tasks = st.session_state.saved_tasks + st.session_state.applied_tasks

if len(all_tasks) > 0:
    category_counts = {}
    for task in all_tasks:
        category_counts[task["category"]] = category_counts.get(task["category"], 0) + 1

    df = pd.DataFrame(
        {"Category": list(category_counts.keys()), "Count": list(category_counts.values())}
    )

    fig = px.bar(df, x="Category", y="Count", color="Category", text="Count")
    fig.update_layout(showlegend=False)
    st.subheader("Your Tasks by Category")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Start saving or applying to tasks to generate dashboard insights.")

status_counts = {"Applied": 0, "Matched": 0, "Assigned": 0, "In Progress": 0, "Completed": 0}
for task in st.session_state.applied_tasks:
    if task["status"] in status_counts:
        status_counts[task["status"]] += 1

status_df = pd.DataFrame(
    {"Status": list(status_counts.keys()), "Count": list(status_counts.values())}
)

fig2 = px.pie(status_df, names="Status", values="Count", hole=0.55)
st.subheader("Task Progress Breakdown")
st.plotly_chart(fig2, use_container_width=True)
