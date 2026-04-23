import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Startup Dashboard", page_icon="🏢", layout="wide")

st.title("🏢 Startup Dashboard")
st.caption("Track posted roles, applicants, and category demand at a glance.")

col1, col2, col3 = st.columns(3)
col1.metric("Open Roles", 4)
col2.metric("Applicants", 18)
col3.metric("Avg Pay", "CHF 1.6k")

data = pd.DataFrame({
    "Job": ["Marketing", "Product", "Design"],
    "Applicants": [8, 6, 4]
})

fig = px.bar(
    data,
    x="Job",
    y="Applicants",
    color="Job",
    text="Applicants"
)
fig.update_layout(showlegend=False)

st.subheader("Applicants per Job")
st.plotly_chart(fig, use_container_width=True)

