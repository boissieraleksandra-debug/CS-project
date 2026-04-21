import streamlit as st

st.title("❤️ Liked Jobs")

liked_jobs = [
    "Marketing Intern at GrowthAI",
    "Product Intern at TechFlow"
]

for job in liked_jobs:
    st.write("✔️", job)
