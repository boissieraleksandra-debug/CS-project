"""
app.py — Landing page (the very first screen).

The user picks their role here. Their choice is stored in
st.session_state and used by every other page to decide what to show.

We also call init_db() so a teammate who clones the repo and just runs
`streamlit run app.py` (forgetting `python seed.py`) at least gets an
empty-but-valid database.
"""

import streamlit as st #for the user interface

import auth #for restoring login state and logging out
import ui #for loading our custom CSS and rendering the sidebar
from db import init_db #create the database if it doesn't exist yet, so the app doesn't break for a teammate who forgets to run seed.py first

st.set_page_config(
    page_title="Profile · gigly",
    page_icon="g",
    layout="centered",
    initial_sidebar_state="expanded",
) # Configures the browser tab with our visual identity 


init_db()
auth.restore_login() #checks if the user was already logged in and restores their session state if so 
ui.load_css() # load our custom CSS we wrote in page sytle.css
ui.sidebar() # aplly the sidebar navigation

# ---- Hero ---------------------------------------------------------------
st.markdown( # Render the hero banner using raw HTML so we can apply our visual design, the divider are the one we disigned in the CSS
    """
    <div class='gigly-hero'>
      <div class='gigly-hero-mark'>gigly</div>
      <div class='gigly-hero-sub'>Where students and startups build together.</div>
      <div class='gigly-hero-meta'>Short-term roles. Real work. No noise.</div> 
    </div>
    """,
    unsafe_allow_html=True, # this line is required to inject HTML through st.markdown() as streamlit bloack HTML by default
)
st.write("")

# ---- Already logged in? Offer a continue link --------------------------
role = st.session_state.get("role")

if role == "student" and st.session_state.get("student_id"): # checks if the user is logged in as a student by looking for the student_id, which is set at login
    st.success("Signed in as a student.")
    if st.button("Continue to Discover", type="primary", use_container_width=True):
        st.switch_page("pages/2_Discovery.py")
    if st.button("Log out", use_container_width=True):
        auth.clear_login()
        for k in ("profile_editing", "mode"):
            st.session_state.pop(k, None)
        st.rerun()
    st.stop() # If the user is already logged in, we show a success message and offer a button to continue to the appropriate page based on their role. We also offer a logout button that clears their session state and reruns the app to show the landing page again.

if role == "startup" and st.session_state.get("startup_id"):
    st.success("Signed in as a startup.")
    if st.button("Continue to Listings", type="primary", use_container_width=True):
        st.switch_page("pages/6_Startup_Listings.py")
    if st.button("Log out", use_container_width=True):
        auth.clear_login()
        for k in ("profile_editing", "startup_editing", "mode"):
            st.session_state.pop(k, None)
        st.rerun()
    st.stop() # Same logic as above but for startup users. We check for startup_id to confirm they're logged in as a startup, and offer navigation to the appropriate page or logout.

# ---- Role picker -------------------------------------------------------
st.markdown("### Get started")

col1, col2 = st.columns(2) # Two-column role picker with buttons for "I'm a student" and "I'm a startup". When the user clicks one, we save their choice in session_state and navigate to the appropriate profile creation page. We also set the first button to type="primary" to visually emphasize it as the most common user path, but both options are equally valid.

with col1:
    if st.button("I'm a student", use_container_width=True, type="primary"):
        st.session_state["role"] = "student"
        st.switch_page("pages/1_Profile.py")

with col2:
    if st.button("I'm a startup", use_container_width=True):
        st.session_state["role"] = "startup"
        st.switch_page("pages/5_Startup_Profile.py")

st.write("")
st.caption(
    "Students build a profile, browse a personalized feed, and apply with one click. "
    "Startups post listings, review applicants, and hire fast."
)
