import streamlit as st
import pandas as pd
import plotly.express as px
from app_data import initialize_state
from ui import apply_global_styles, page_header

st.set_page_config(page_title="Startup Dashboard", page_icon="🏢", layout="wide")

initialize_state()
apply_global_styles()
page_header("🏢 Startup Dashboard", "See open tasks, applicant activity, and which categories attract the most interest.")

open_roles = len(st.session_state.tasks)
applicants = len(st.session_state.applied_tasks)
avg_pay = "CHF 270"

col1, col2, col3 = st.columns(3)
col1.metric("Open Tasks", open_roles)
col2.metric("Applicants", applicants)
col3.metric("Average Pay", avg_pay)

category_counts = {}
for task in st.session_state.tasks:
    category_counts[task["category"]] = category_counts.get(task["category"], 0) + 1

df = pd.DataFrame(
    {"Category": list(category_counts.keys()), "Open Tasks": list(category_counts.values())}
)

fig = px.bar(df, x="Category", y="Open Tasks", color="Category", text="Open Tasks")
fig.update_layout(showlegend=False)

st.subheader("Open Tasks by Category")
st.plotly_chart(fig, use_container_width=True)

if len(st.session_state.applied_tasks) == 0:
    st.info("No applicants yet.")
else:
    st.subheader("Recent Applicants")
    for task in st.session_state.applied_tasks:
        applicant = task.get("applicant", {})
        st.markdown(
            f"""
            <div class="app-card">
                <div class="task-title">{task['title']}</div>
                <div class="task-startup">Applicant: {applicant.get('full_name', 'Unknown')}</div>
                <div class="task-description">
                    Status: <b>{task['status']}</b><br>
                    Email: {applicant.get('email', '-')}<br>
                    CV: {applicant.get('cv_name', '-')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
