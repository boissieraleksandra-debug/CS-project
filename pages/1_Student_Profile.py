import streamlit as st
from data import init

init()

if st.session_state.role != "student":
    st.stop()

st.title("👤 Student Profile")

name = st.text_input("Your Name")

if st.button("Save"):
    st.session_state.student["name"] = name
    st.success("Saved")
