import streamlit as st
from db import init_db, get_startup_profile, save_startup_profile

st.set_page_config(page_title="Startup Profile", page_icon="🏢", layout="wide")
init_db()

if st.session_state.get("role") != "startup":
    st.stop()

st.title("🏢 Startup Profile")

profile = get_startup_profile()

startup_name = st.text_input("Startup Name", value=profile["startup_name"])
industry = st.text_input("Industry", value=profile["industry"])
location = st.text_input("Location", value=profile["location"])
description = st.text_area("Description", value=profile["description"])
contact_email = st.text_input("Contact Email", value=profile["contact_email"])

if st.button("Save Startup Profile", use_container_width=True):
    save_startup_profile({
        "startup_name": startup_name,
        "industry": industry,
        "location": location,
        "description": description,
        "contact_email": contact_email
    })
    st.session_state.startup_name = startup_name
    st.success("Startup profile saved")
