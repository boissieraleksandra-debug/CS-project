import streamlit as st

st.title("👤 Profile")

st.text_input("Full Name")
st.text_input("LinkedIn")
st.text_area("Education")
st.text_area("Interests")
st.text_input("Availability")

st.file_uploader("Upload CV")

st.button("Save Profile")
