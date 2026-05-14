#ui.py centralises what every page needs visually so that changing the sidebar or stylesheet in one place automatically updates the whole app.

import os # for environment variables and file paths
from pathlib import Path # builds file paths that work on any operating system

import streamlit as st #for UI
import auth
from db import list_emails, get_student, get_startup # database functions to fetch data

try: # 'try' to prevent the app to crash if dotenv is not installed
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
# Load .env so API keys are available or skipped if dotenv isn't installed.
CSS_PATH = Path(__file__).parent / "static" / "style.css" # build path to stylesheet relative to this file 


def load_css():
    if CSS_PATH.exists():
        css = CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
# This function loads the CSS file and injects it into the Streamlit app using st.markdown(). This allows us to apply our custom styles defined in style.css across the entire app. We use unsafe_allow_html=True to allow raw HTML/CSS injection, which is necessary for this to work.

def industry_class(industry):
    if not industry:
        return ""
    known = {"marketing", "technology", "finance", "sustainability", "design"}
    slug = industry.strip().lower() # makes it lowercase and removes extra spaces
    return slug if slug in known else ""
# Return a CSS class slug for known industries only and unknown industries get no class so they don't break our styling

def sidebar(): # these lines open the sidebar and render brand logo at the top 
    role = st.session_state.get("role")

    with st.sidebar:
        st.markdown(
            "<div class='gigly-wordmark'>gigly</div>"
            "<div class='gigly-tagline'>Students × Startups</div>",
            unsafe_allow_html=True,
        )

        if role == "student": # show different navigation links in the sidebar based on the user's role, which we have in session_state. 
            st.page_link("pages/1_Profile.py",           label="Profile")
            st.page_link("pages/2_Discovery.py",         label="Discover")
            st.page_link("pages/3_Liked_Jobs.py",        label="Saved")
            st.page_link("pages/4_Student_Dashboard.py", label="Dashboard")
        elif role == "startup":
            st.page_link("pages/5_Startup_Profile.py",      label="Company")
            st.page_link("pages/6_Startup_Listings.py",     label="Listings")
            st.page_link("pages/7_Startup_Applications.py", label="Applicants")
            st.page_link("pages/8_Startup_Dashboard.py",    label="Dashboard")
        else:
            st.page_link("app.py", label="Home") # if no role is selected, we just show a link to the home page  (landing page) 

        st.divider()

        # show only emails sent to the logged-in user
        user_email = None # if no user is found, the inbox shows nothing
        if role == "student" and st.session_state.get("student_id"):
            student = get_student(st.session_state["student_id"])
            if student:
                user_email = student["email"]
        elif role == "startup" and st.session_state.get("startup_id"):
            startup = get_startup(st.session_state["startup_id"])
            if startup:
                user_email = startup["email"]

        real_mode = bool(os.getenv("BREVO_API_KEY", "").strip())
        mode_label = "Live delivery (Brevo)" if real_mode else "Simulated mode"

        with st.expander("Inbox", expanded=False):
            st.caption(mode_label)
            emails = list_emails(limit=10, to_email=user_email)
            if not emails:
                st.caption("No messages yet.")
            else:
                for e in emails:
                    status = "Sent" if e["sent_ok"] else "Failed"
                    st.markdown(f"**{e['subject']}**")
                    st.caption(f"{status} · To: {e['to_email']} · {e['created_at']}")
                    with st.expander("Read", expanded=False):
                        st.text(e["body"])
                    st.divider()
        # Collapsible inbox showing last 10 emails for this user.
        # mode_label shows whether emails are really being sent or just logged. 

        #log out button
        if role: # only show the logout button if a role is selected (so if the user is logged in)
            if st.button("Log out", use_container_width=True):
                auth.clear_login() # removes the login data
                for k in ("profile_editing", "startup_editing", "mode",
                          "expanded_job", "viewing_application_id",
                          "new_job_form_open"):
                    st.session_state.pop(k, None)
                st.switch_page("app.py")
