import streamlit as st
from db import init_db, seed_tasks

st.set_page_config(page_title="SkillSwipe", page_icon="🚀", layout="wide")

# INIT DB
init_db()
seed_tasks()

# SESSION DEFAULTS
if "role" not in st.session_state:
    st.session_state.role = None

# ROLE SELECTION
if st.session_state.role is None:
    st.title("🚀 Welcome to SkillSwipe")

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

# HEADER
st.sidebar.title("Navigation")

if st.session_state.role == "student":
    st.sidebar.success("Logged as Student")
    st.sidebar.page_link("pages/1_Profile.py", label="Profile")
    st.sidebar.page_link("pages/2_Discover.py", label="Discover")
    st.sidebar.page_link("pages/3_LikedJobs.py", label="Liked Jobs")
    st.sidebar.page_link("pages/4_Task_Progress.py", label="Task Progress")
    st.sidebar.page_link("pages/5_StudentDashboard.py", label="Dashboard")

if st.session_state.role == "startup":
    st.sidebar.success("Logged as Startup")
    st.sidebar.page_link("pages/6_Startup_Profile.py", label="Profile")
    st.sidebar.page_link("pages/7_Post_Task.py", label="Post Task")
    st.sidebar.page_link("pages/8_Applicants.py", label="Applicants")
    st.sidebar.page_link("pages/6_StartupDashboard.py", label="Dashboard")

if st.sidebar.button("🔄 Switch Role"):
    st.session_state.role = None
    st.rerun()

# HOME PAGE
st.title("SkillSwipe")
st.write("Use the sidebar to navigate.")
