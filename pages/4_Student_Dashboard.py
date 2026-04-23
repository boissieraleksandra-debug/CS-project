import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Student Dashboard", page_icon="📊", layout="wide")

st.title("📊 Student Dashboard")
st.caption("Your activity, progress, and strongest startup matches in one place.")

col1, col2, col3 = st.columns(3)
col1.metric("Tasks Viewed", 12)
col2.metric("Tasks Liked", len(st.session_state.get("liked_jobs", [])))
col3.metric("Applications Sent", len(st.session_state.get("applied_jobs", [])))

data = pd.DataFrame({
    "Category": ["Marketing", "Product", "Design"],
    "Likes": [3, 1, 1]
})

fig = px.bar(
    data,
    x="Category",
    y="Likes",
    color="Category",
    text="Likes"
)
fig.update_layout(showlegend=False)

st.subheader("Liked Tasks by Category")
st.plotly_chart(fig, use_container_width=True)

