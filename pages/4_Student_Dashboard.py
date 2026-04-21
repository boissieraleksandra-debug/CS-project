import streamlit as st
import pandas as pd

st.title("📊 Student Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Jobs Viewed", 12)
col2.metric("Jobs Liked", 5)
col3.metric("Avg Match Score", "85%")

data = pd.DataFrame({
    "Category": ["Marketing", "Product", "Design"],
    "Likes": [3, 1, 1]
})

st.subheader("Liked Jobs by Category")
st.bar_chart(data.set_index("Category"))
