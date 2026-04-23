import streamlit as st
from data import init

st.set_page_config(layout="wide")
init()

st.title("🚀 SkillSwipe")

if st.session_state.role is None:
    st.subheader("Who are you?")

    col1, col2 = st.columns(2)

    if col1.button("🎓 I am a Student", use_container_width=True):
        st.session_state.role = "student"
        st.rerun()

    if col2.button("🏢 I am a Startup", use_container_width=True):
        st.session_state.role = "startup"
        st.rerun()

else:
    st.success(f"Logged in as {st.session_state.role}")
    st.info("Use sidebar to navigate")
