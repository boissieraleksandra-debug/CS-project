import streamlit as st
from db import init_db, seed_tasks

st.set_page_config(page_title="SkillSwipe", page_icon="🚀", layout="wide")

init_db()
seed_tasks()

if "role" not in st.session_state:
    st.session_state.role = None

st.title("🚀 SkillSwipe")

if st.session_state.role is None:
    st.subheader("Choose your role")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 I am a Student", use_container_width=True):
            st.session_state.role = "student"
            st.session_state.student_name = "Student Demo"
            st.rerun()

    with col2:
        if st.button("🏢 I am a Startup", use_container_width=True):
            st.session_state.role = "startup"
            st.session_state.startup_name = "Startup Demo"
            st.rerun()

    st.stop()

st.success(f"Current role: {st.session_state.role.title()}")
st.info("Use the sidebar to open your pages.")

if st.sidebar.button("🔄 Switch Role"):
    st.session_state.role = None
    st.rerun()
