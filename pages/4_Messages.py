import streamlit as st

st.title("💬 Messages / Contact")

startup = st.text_input("Startup Name")
message = st.text_area("Write your message")

if st.button("Send Message"):
    st.success(f"Message sent to {startup}.")
