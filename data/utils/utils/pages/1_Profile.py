import streamlit as st

st.title("👤 Student Profile")

if "profile" not in st.session_state:
    st.session_state.profile = {
        "full_name": "",
        "linkedin": "",
        "education": "",
        "interests": "",
        "availability": ""
    }

full_name = st.text_input("Full Name", st.session_state.profile["full_name"])
linkedin = st.text_input("LinkedIn Profile", st.session_state.profile["linkedin"])
cv_file = st.file_uploader("Upload CV", type=["pdf", "docx"])
education = st.selectbox("Education", ["", "Business", "Design", "Economics", "Communications"])
interests = st.text_input("Interests (example: Marketing, Design, Data)")
availability = st.selectbox("Availability", ["", "Part-time", "Flexible", "Full-time"])

if st.button("Save Profile"):
    st.session_state.profile = {
        "full_name": full_name,
        "linkedin": linkedin,
        "education": education,
        "interests": interests,
        "availability": availability
    }
    st.success("Profile saved successfully.")

if cv_file is not None:
    st.info(f"Uploaded CV: {cv_file.name}")
