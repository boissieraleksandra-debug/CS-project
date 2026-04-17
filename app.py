import streamlit as st

st.set_page_config(
    page_title="Student Startup Match",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Student Startup Match")
st.write("A mobile-style prototype for matching students with startup jobs.")

st.markdown("""
### Pages in this app
Use the sidebar to open:
- Profile
- Discover
- Liked Jobs
- Messages
- Student Dashboard
- Startup Dashboard
""")

st.info("Start by filling in the Profile page.")
