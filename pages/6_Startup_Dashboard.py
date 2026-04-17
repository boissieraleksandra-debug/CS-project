import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_jobs

st.title("🏢 Startup Dashboard")

jobs = load_jobs()
liked_jobs = st.session_state.get("liked_jobs", [])

open_roles = len(jobs)
interested_students = len(liked_jobs)

col1, col2 = st.columns(2)
col1.metric("Open Roles", open_roles)
col2.metric("Interested Students", interested_students)

if liked_jobs:
    liked_df = pd.DataFrame(liked_jobs)
    applicant_counts = liked_df["title"].value_counts().reset_index()
    applicant_counts.columns = ["Job Title", "Applicants"]

    fig1 = px.bar(
        applicant_counts,
        x="Job Title",
        y="Applicants",
        title="Applicants per Job",
        color="Job Title"
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No interested students yet.")

pay_df = jobs.groupby("category", as_index=False)["pay_rate"].mean()

fig2 = px.bar(
    pay_df,
    x="category",
    y="pay_rate",
    title="Average Pay by Category",
    color="category"
)
st.plotly_chart(fig2, use_container_width=True)
