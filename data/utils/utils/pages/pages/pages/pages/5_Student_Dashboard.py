import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Student Dashboard")

liked_jobs = st.session_state.get("liked_jobs", [])
passed_jobs = st.session_state.get("passed_jobs", [])

jobs_viewed = len(liked_jobs) + len(passed_jobs)
jobs_liked = len(liked_jobs)

if liked_jobs:
    liked_df = pd.DataFrame(liked_jobs)
    top_category = liked_df["category"].mode()[0]
    avg_match_score = round(liked_df["match_score"].mean(), 1)
else:
    liked_df = pd.DataFrame()
    top_category = "N/A"
    avg_match_score = 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Jobs Viewed", jobs_viewed)
col2.metric("Jobs Liked", jobs_liked)
col3.metric("Top Category", top_category)
col4.metric("Avg Match Score", avg_match_score)

if not liked_df.empty:
    category_counts = liked_df["category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]

    fig = px.bar(
        category_counts,
        x="Category",
        y="Count",
        title="Liked Jobs by Category",
        color="Category"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Like some jobs to see your dashboard analytics.")
