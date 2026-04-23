import streamlit as st
from db import init_db, get_student_profile, save_student_profile

st.set_page_config(page_title="Student Profile", page_icon="👤", layout="wide")
init_db()

if st.session_state.get("role") != "student":
    st.stop()

st.title("👤 Student Profile")

profile = get_student_profile()

full_name = st.text_input("Full Name", value=profile["full_name"])
linkedin = st.text_input("LinkedIn", value=profile["linkedin"])
education = st.text_input("Education", value=profile["education"])
availability = st.text_input("Availability", value=profile["availability"])
interests = st.text_area("Interests", value=profile["interests"])
bio = st.text_area("Bio", value=profile["bio"])
cv = st.file_uploader("Upload CV")

if st.button("Save Profile", use_container_width=True):
    cv_name = cv.name if cv is not None else profile["cv_name"]

    save_student_profile({
        "full_name": full_name,
        "linkedin": linkedin,
        "education": education,
        "availability": availability,
        "interests": interests,
        "bio": bio,
        "cv_name": cv_name
    })

    st.session_state.student_name = full_name
    st.success("Profile saved")
