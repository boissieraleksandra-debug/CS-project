import streamlit as st
from app_data import initialize_state
from ui import apply_global_styles

st.set_page_config(
    page_title="SkillSwipe",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_state()
apply_global_styles()

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">Find startup work that actually fits you.</div>
        <div class="hero-subtitle">
            SkillSwipe connects students with flexible, short-term startup tasks in marketing,
            design, strategy, research, and operations — all in a clean mobile-style experience.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
col1.metric("Active tasks", len(st.session_state.tasks))
col2.metric("Saved tasks", len(st.session_state.saved_tasks))
col3.metric("Applied tasks", len(st.session_state.applied_tasks))

st.markdown("## Why SkillSwipe works")
st.markdown(
    """
    <div class="app-card">
        <b>Students</b> discover relevant startup work quickly.<br><br>
        <b>Startups</b> find flexible talent for short tasks without a full hiring process.<br><br>
        <b>The app</b> becomes smarter by using profile data, likes, and applications to shape recommendations.
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("Use the sidebar to open Profile, Discover Tasks, Saved Tasks, Task Progress, and the dashboards.")
