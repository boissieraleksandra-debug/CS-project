import streamlit as st
from db import init_db, seed_tasks

st.set_page_config(page_title="SkillSwipe", page_icon="🚀", layout="wide")

init_db()
seed_tasks()

if "role" not in st.session_state:
    st.session_state.role = None

st.write("# 🚀 SkillSwipe")
st.write("Choose your role to start using the app.")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎓 I am a Student", use_container_width=True):
        st.session_state.role = "student"
        st.rerun()

with col2:
    if st.button("🏢 I am a Startup", use_container_width=True):
        st.session_state.role = "startup"
        st.rerun()

if st.session_state.role:
    st.success(f"Current role: {st.session_state.role}")

    if st.button("Reset Role"):
        st.session_state.role = None
        st.rerun()

st.write("Then use the sidebar pages.")
