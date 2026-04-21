import streamlit as st
import pandas as pd

st.title("🏢 Startup Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Open Roles", 4)
col2.metric("Applicants", 18)
col3.metric("Avg Pay", "CHF 1600")

data = pd.DataFrame({
    "Job": ["Marketing", "Product", "Design"],
    "Applicants": [8, 6, 4]
})

st.subheader("Applicants per Job")
st.bar_chart(data.set_index("Job"))
