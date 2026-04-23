import streamlit as st

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #F8FAFF 0%, #F3F5FB 100%);
    }

    .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("👤 My Profile")
st.caption("Build your student profile so SkillSwipe can recommend the best startup tasks.")

full_name = st.text_input("Full Name")
linkedin = st.text_input("LinkedIn")
education = st.selectbox(
    "Education",
    ["Business", "Marketing", "Design", "Economics", "Computer Science", "Other"]
)
availability = st.selectbox(
    "Availability",
    ["Part-time", "Flexible", "Weekends", "Evenings", "Full-time"]
)
interests = st.text_area("Interests")
bio = st.text_area("Short Bio")
cv = st.file_uploader("Upload CV", type=["pdf", "docx"])

if st.button("Save Profile", use_container_width=True):
    st.success("Profile saved.")

