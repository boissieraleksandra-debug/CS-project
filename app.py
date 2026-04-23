import streamlit as st
from db import init_db, seed_tasks
from ui import apply_styles

st.set_page_config(
    page_title="SkillSwipe",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
seed_tasks()
apply_styles()

if "role" not in st.session_state:
    st.session_state.role = None

st.markdown("""
<div class="hero-card">
    <div class="hero-title">SkillSwipe</div>
    <div class="hero-subtitle">
        A polished two-sided startup task app where students discover opportunities and startups hire fast for real short-term work.
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.role is None:
    st.subheader("Choose your side")
    st.caption("This prototype supports both student and startup journeys.")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎓 I am a Student", use_container_width=True):
            st.session_state.role = "student"
            st.rerun()

    with col2:
        if st.button("🏢 I am a Startup", use_container_width=True):
            st.session_state.role = "startup"
            st.rerun()

else:
    st.success(f"Current role: {st.session_state.role.title()}")
    c1, c2 = st.columns([4, 1])

    with c1:
        st.info("Use the sidebar to open your pages.")
    with c2:
        if st.button("Switch Role", use_container_width=True):
            st.session_state.role = None
            st.rerun()
