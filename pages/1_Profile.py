import streamlit as st
from app_data import initialize_state
from ui import apply_global_styles, page_header

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

initialize_state()
apply_global_styles()
page_header("👤 My Profile", "Build your student profile so SkillSwipe can recommend the best startup tasks.")

profile = st.session_state.profile

full_name = st.text_input("Full Name", value=profile["full_name"])
linkedin = st.text_input("LinkedIn", value=profile["linkedin"])
education = st.selectbox(
    "Education",
    ["", "Business", "Marketing", "Design", "Economics", "Computer Science", "Other"],
    index=0 if profile["education"] == "" else ["", "Business", "Marketing", "Design", "Economics", "Computer Science", "Other"].index(profile["education"]),
)
availability = st.selectbox(
    "Availability",
    ["", "Part-time", "Flexible", "Weekends", "Evenings", "Full-time"],
    index=0 if profile["availability"] == "" else ["", "Part-time", "Flexible", "Weekends", "Evenings", "Full-time"].index(profile["availability"]),
)
interests = st.text_area("Interests", value=profile["interests"], placeholder="e.g. startups, social media, UX, research")
bio = st.text_area("Short Bio", value=profile["bio"], placeholder="A short sentence about who you are and what you enjoy working on.")
cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

col1, col2 = st.columns(2)

with col1:
    if st.button("Save Profile", use_container_width=True):
        st.session_state.profile = {
            "full_name": full_name,
            "linkedin": linkedin,
            "education": education,
            "availability": availability,
            "interests": interests,
            "bio": bio,
            "cv_name": cv.name if cv is not None else profile["cv_name"],
        }
        st.success("Profile saved successfully.")

with col2:
    if st.button("Load Example Profile", use_container_width=True):
        st.session_state.profile = {
            "full_name": "Aleksandra Boissier",
            "linkedin": "linkedin.com/in/example",
            "education": "Business",
            "availability": "Part-time",
            "interests": "marketing, startups, strategy, design",
            "bio": "Business student interested in startup work, marketing, strategy, and product ideas.",
            "cv_name": "cv_aleksandra.pdf",
        }
        st.rerun()

st.markdown("## Profile Preview")
preview = st.session_state.profile

st.markdown(
    f"""
    <div class="app-card">
        <div class="task-title">{preview['full_name'] or 'Your Name'}</div>
        <div class="task-startup">🎓 {preview['education'] or 'Education not set'}</div>
        <div class="task-description">{preview['bio'] or 'Add a short bio to strengthen your profile.'}</div>
        <span class="pill neutral-pill">🔗 {preview['linkedin'] or 'No LinkedIn added'}</span>
        <span class="pill neutral-pill">⏰ {preview['availability'] or 'Availability not set'}</span>
        <span class="pill neutral-pill">📄 {preview['cv_name'] or 'No CV uploaded'}</span>
        <span class="pill match-pill">✨ Interests: {preview['interests'] or 'No interests added'}</span>
    </div>
    """,
    unsafe_allow_html=True,
)
