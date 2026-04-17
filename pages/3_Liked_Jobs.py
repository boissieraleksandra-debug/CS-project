import streamlit as st
import pandas as pd

st.title("❤️ Liked Jobs")

liked_jobs = st.session_state.get("liked_jobs", [])

if liked_jobs:
    df = pd.DataFrame(liked_jobs)
    st.dataframe(df[["title", "startup_name", "category", "pay_rate", "location", "match_score"]])
else:
    st.info("No liked jobs yet.")
