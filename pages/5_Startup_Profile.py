"""
5_Startup_Profile.py — Startup company profile (signup OR view/edit).

Same two-mode pattern as 1_Profile.py for students:
  - No startup_id in session_state → show the signup form.
  - startup_id present → show the saved profile (view) with an Edit toggle.
"""

import streamlit as st
from pathlib import Path

# The rest that will come is to link everything and make sure it's saved in db: -> this is the code that is also written on the top of the student profile page 
import ui                                       # sets the theme and the buttons in the sidebar for all pages
from db import (                                # this is the database where the company profiles will be saved and can be edited
    init_db,
    create_startup,
    update_startup,
    get_startup,
    get_startup_by_email,
)
from mailer import send_email                   # sends the welcome email
from templates import signup_confirm_startup    # the welcome-email body

# ---- Page setup ---------------------------------------------------------
# this has to be on the top of every pages since it sets the theme of every page
# and the overall layout (we want the centered mobile-style layout). same for sutdent profile
st.set_page_config(
    page_title="Company · gigly",
    page_icon="g",
    layout="centered",
    initial_sidebar_state="expanded",
) #basically it sets the name of the app and where should it be positioned
init_db()        # makes sure app.db exists (safe to call every time)
ui.load_css()    # applies the purple theme
ui.sidebar()     # draws the left sidebar (Company / Listings / Applicants / Dashboard)

# Where uploaded logos go on disk: <project>/uploads/startup_<id>.png
# We use the same folder throughout the app
UPLOADS = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS.mkdir(exist_ok=True)

# Visiting this page directly counts as picking "I'm a startup"
if st.session_state.get("role") != "startup":
    st.session_state["role"] = "startup"

# the part is giving the opportunity to edit their profile 
if "mode" not in st.session_state:
    st.session_state.mode = "edit"

INDUSTRY_OPTIONS = [
    "Finance",
    "Technology",
    "Design",
    "Legal",
    "Human Resources",
    "Consulting",
    "Sustainability",
    "Marketing",
    "Data & Analytics",
    "Other",
]

#====================================================
#FORM for profile for startups
#====================================================

#we want to have the feature that whenever the company account is done, the startup can go and edit their company profile on the app.
#we want to show the saved profile when they click on company.
#if we don't do it then everytime the startup wants to change a small thing on the profile, it has to redo the whole form because the form is empty
if st.session_state.role == "startup" and st.session_state.get("startup_id"): #means that if the role is equal to startup and associated to a startup id
    #it goes and look it up on the database using the id
    startup = get_startup(st.session_state["startup_id"])

    #if the database doesn't have this id then let the "normal" sign up form pop up
    if not startup:
        st.session_state.pop("startup_id", None)
    else:
        if st.session_state.mode == "edit":
            st.title("Edit your Company Profile")

            company_name = st.text_input("Company name", value=startup["name"])
            st.markdown(f"Email: {startup['email']} (can't be changed)") #email is the unique key in the db, we don't let users change it

            website = st.text_input("Website", value=startup["website"] or "")

            #find the index of the saved industry so the dropdown opens on it
            saved_industry_index = (
                INDUSTRY_OPTIONS.index(startup["industry"])
                if startup["industry"] in INDUSTRY_OPTIONS else 0
            )
            industry = st.selectbox(
                "Industry",
                options=INDUSTRY_OPTIONS,
                index=saved_industry_index,
            )

            description = st.text_area(
                "Short description of the startup",
                value=startup["description"] or "",
            )

            logo = st.file_uploader(
                "Company logo",
                type=["png", "jpg", "jpeg"],
            )
            if logo is not None:
                st.image(logo, width=150)

            col_back, col_save = st.columns(2)
            with col_back: #to have a button that cancel changes if needed
                if st.button("Cancel", use_container_width=True):
                    st.session_state.mode = "view"
                    st.rerun()

            with col_save:
                if st.button("Save Profile", use_container_width=True):
                    #only the company name is still required
                    if not company_name.strip():
                        st.error("Company name is required.")
                        st.stop()

                    #update the existing row in the database (NOT create_startup)
                    update_startup(
                        startup["id"],
                        name=company_name.strip(),
                        website=website.strip() or None,
                        industry=industry,
                        description=description.strip() or None,
                    )

                    #if they uploaded a new logo, save it and update the filename
                    if logo is not None:
                        logo_filename = f"startup_{startup['id']}.png"
                        (UPLOADS / logo_filename).write_bytes(logo.getvalue())
                        update_startup(startup["id"], logo_filename=logo_filename)

                    #done - back to view mode
                    st.session_state.mode = "view"
                    st.success("Profile updated.")
                    st.rerun()

        # this is when they are on the profile tab of the app in the sidebar and they are viewing the profile + have an edit button
        else:
            st.title(startup['name'])
            st.caption("This is what students see when you post a role.")
            st.markdown(f"**Industry:**  {startup['industry'] or '—'}")
            st.markdown(f"**Email:**  {startup['email']}")
            st.markdown(f"**Website:**  {startup['website'] or '—'}")
            st.markdown("**About:**")
            st.write(startup['description'] or '—')
            st.markdown(f"**Logo:**  {startup['logo_filename'] or '—'}")

            if st.button("Edit Profile", type="primary", use_container_width=True):
                st.session_state.mode = "edit"
                st.rerun()

        st.stop()  #after either branch, stop so the signup form below doesn't render

#now we create the opening of the form once the user clicks on the button startup
#it's basically the same code or same logic as the form for students
if st.session_state.role == "startup" and st.session_state.mode == "edit":
    st.title("Startup Profile")

    # --- Returning startup: sign in by email only ---
    st.markdown("**Already registered?** Enter your email to sign back in.")
    returning_email = st.text_input("Your registered email", key="returning_email")
    if st.button("Sign in", use_container_width=True):
        if returning_email.strip():
            existing = get_startup_by_email(returning_email.strip())
            if existing:
                st.session_state["role"] = "startup"
                st.session_state["startup_id"] = existing["id"]
                st.session_state.mode = "view"
                st.switch_page("pages/5_Startup_Profile.py")
            else:
                st.error("No account found with that email. Fill the form below to create one.")
        else:
            st.warning("Please enter your email.")

    st.divider()
    st.markdown("**New here?** Create your company profile below.")
    #now we start with the company name and the website which are text box
    company_name = st.text_input("Company name")
    website = st.text_input("Website")
    #now we have to write the industry and we want to do a select branch
    industry = st.selectbox(
        "Industry",
        options=INDUSTRY_OPTIONS,
    )
    #okay now we want a company description
    description = st.text_area(
        "Short description of the startup",
    )
    #now we want the email
    email = st.text_input("Contact email")

    #now we want the logo (same as for the picture for the students)
    logo = st.file_uploader(
        "Company logo",
        type=["png", "jpg", "jpeg"],
    )
    if logo is not None:
        st.image(logo, width=150)

    #bottom bar with button "back" and button "save profile"
    col_back, col_save_profile = st.columns(2)

    with col_back:
        if st.button("Back", use_container_width=True, key="startup_back"):
            st.session_state.role = None #you forget the chosen role
            st.session_state.mode = "edit" #reset to edit for next time
            st.switch_page("app2.py") #go back to the landing page

    #when the startup wants to save its profile
    with col_save_profile:
        if st.button("Save Profile", use_container_width=True, key="startup_save_profile"):
            #we want the startup to give us at least the company name and the email otherwise we won't save the profile:
            if not company_name.strip() or not email.strip():
                st.error("Company name and email are required.")
                st.stop()

            #if a profile with this email already exists, don't create a new account but just sign back in
            existing = get_startup_by_email(email.strip())
            if existing:
                st.session_state["role"] = "startup"
                st.session_state["startup_id"] = existing["id"]
                st.session_state.mode = "view" #default to view mode for returning startups
                st.info("Welcome back!")
                st.switch_page("pages/6_Startup_Listings.py")

            #okay now if the company gave its name and email and isn't an already existing user, we want to save its profile
            #we need to create the profile, store it into the database and make sure that it goes into the startups table
            startup_id = create_startup(
                name=company_name.strip(),
                email=email.strip(),
                phone=None,
                industry=industry,
                description=description.strip() or None,
                website=website.strip() or None,
            )

            #if a logo was uploaded, save it to disk as uploads/startup_<id>.png then update the database row so it knows the filename
            if logo is not None:
                logo_filename = f"startup_{startup_id}.png"
                (UPLOADS / logo_filename).write_bytes(logo.getvalue())
                update_startup(startup_id, logo_filename=logo_filename)

            #now we need to tell the rest of the app who is logged in. the company must appear in the other pages and "on the other side"
            st.session_state["role"] = "startup"
            st.session_state["startup_id"] = startup_id
            st.session_state.mode = "view" #default to view mode after signup so coming back to Company shows the saved info

            #once they are logged in and everything is saved, the startup needs to receive the welcome email
            startup_row = get_startup(startup_id)
            subject, body = signup_confirm_startup(startup_row)
            send_email(startup_row["email"], subject, body)

            #send the company to the listings page (where they can post their first role)
            st.success("Profile created. Check your inbox for the confirmation email.")
            st.switch_page("pages/6_Startup_Listings.py")
