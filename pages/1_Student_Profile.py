import streamlit as st
from db import init_db, get_student_profile, save_student_profile
from ui import apply_styles, header

st.set_page_config(page_title="Student Profile", page_icon="👤", layout="wide")
init_db()
apply_styles()

if st.session_state.get("role") != "student":
    st.stop()

header("👤 Student Profile", "Create your profile so SkillSwipe can recommend the most relevant startup tasks.")

profile = get_student_profile()

education_options = ["", "Business", "Marketing", "Design", "Economics", "Computer Science", "Other"]
availability_options = ["", "Part-time", "Flexible", "Weekends", "Evenings", "Full-time"]

full_name = st.text_input("Full Name", value=profile["full_name"])
linkedin = st.text_input("LinkedIn", value=profile["linkedin"])
education = st.selectbox(
    "Education",
    education_options,
    index=education_options.index(profile["education"]) if profile["education"] in education_options else 0
)
availability = st.selectbox(
    "Availability",
    availability_options,
    index=availability_options.index(profile["availability"]) if profile["availability"] in availability_options else 0
)
interests = st.text_area("Interests", value=profile["interests"], placeholder="e.g. marketing, startups, UX, research")
bio = st.text_area("Short Bio", value=profile["bio"], placeholder="Tell startups what you enjoy working on.")
cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

col1, col2 = st.columns(2)

with col1:
    if st.button("Save Profile", use_container_width=True):
        save_student_profile({
            "full_name": full_name,
            "linkedin": linkedin,
            "education": education,
            "availability": availability,
            "interests": interests,
            "bio": bio,
            "cv_name": cv.name if cv is not None else profile["cv_name"],
        })
        st.success("Student profile saved.")

with col2:
    if st.button("Load Example Profile", use_container_width=True):
        save_student_profile({
            "full_name": "Aleksandra Boissier",
            "linkedin": "linkedin.com/in/example",
            "education": "Business",
            "availability": "Part-time",
            "interests": "marketing startups strategy design product research",
            "bio": "Business student interested in startup work, strategy, marketing, and product tasks.",
            "cv_name": "Aleksandra_CV.pdf",
        })
        st.success("Example profile loaded.")
        st.rerun()

current = get_student_profile()

st.markdown("## Profile Preview")
st.markdown(f"""
<div class="app-card">
    <div class="task-title">{current['full_name'] or 'Your Name'}</div>
    <div class="task-startup">🎓 {current['education'] or 'Education not set'}</div>
    <div class="task-description">{current['bio'] or 'Add a short bio to improve your profile.'}</div>
    <span class="pill neutral-pill">🔗 {current['linkedin'] or 'No LinkedIn added'}</span>
    <span class="pill neutral-pill">⏰ {current['availability'] or 'Availability not set'}</span>
    <span class="pill neutral-pill">📄 {current['cv_name'] or 'No CV uploaded'}</span>
    <span class="pill soft-pill">✨ Interests: {current['interests'] or 'No interests added'}</span>
</div>
""", unsafe_allow_html=True)
