"""
1_Profile.py — Student profile page (signup OR view/edit).

Two modes, picked at runtime:

1. No student_id in session_state → show the **signup form**.
   On submit: insert the student, send a welcome email, save the
   new id in session, and continue to the Job Feed (Discovery).

2. student_id present → show the **profile** in read-only mode with
   an "Edit" button that switches the same fields into a save-able form.

The signup form is intentionally short so a student can finish in
roughly a minute. The Interests multiselect doubles as input to the
TF-IDF recommender (Phase I).
"""

import streamlit as st
import json   # built-in library to read and write JSON files
import os   # built-in library for handling folders

from pathlib import Path   # built-in library to handle file paths

# These will link all documents together. it has to appear at the top of most pages 
import auth
import ui                                       # sets the theme and the buttons in the sidebar for all pages 
from db import (                                # this is the database where the profiles will be saved and can be edited
    init_db,
    create_student,
    update_student,
    get_student,
    get_student_by_email,
)
from mailer import send_email                   # sends the welcome email
from templates import signup_confirm_student    # the welcome-email body

# ---- Page setup ---------------------------------------------------------
# this has to be on the top of every pages since it sets the theme of every page 
# and the overall layout (we want the centered mobile-style layout).
st.set_page_config(
    page_title="Profile · gigly",
    page_icon="g",
    layout="centered",
    initial_sidebar_state="expanded",
) #basically it sets the name of the app and where should it be positioned
init_db()        # makes sure app.db exists (safe to call every time)
auth.restore_login()
ui.load_css()    # applies the purple theme
ui.sidebar()     # draws the left sidebar (Profile / Discover / Saved / Dashboard)

# Where uploaded CVs go on disk: <project>/uploads/student_<id>.pdf
# We use the same folder throughout the app
UPLOADS = Path(__file__).resolve().parent.parent / "uploads"
UPLOADS.mkdir(exist_ok=True)
#this part means that if no button was chosen the opening page should be shown
if "role" not in st.session_state:
    st.session_state.role = None
#the part below is making hte difference between when the user is viewing the final profile or editing it 
if "mode" not in st.session_state:
    st.session_state.mode = "edit"
#====================================================
#FORM for profile for students
#====================================================

#we want to have the feature that whenever the account is done, the user can go and edit their profile on the app. 
#we want to show the saved profile when they click on profile or settings (idk yet how it's going to be called). 
#if we don't do it then everytime the user wants to change a small thing on the profile, it has to redo the whole form because the form is empty
if st.session_state.role == "student" and st.session_state.get("student_id"): #means that if the role is equal to students and associated to a student id
    #it goes and look it up on the database using the id 
    student = get_student(st.session_state["student_id"])

    #if the database doesn't have this id then let the "normal" sign up form pop up 
    if not student: 
        st.session_state.pop("student_id", None)
    else:
        # ===== EDIT MODE: form pre-filled with saved values =====
        if st.session_state.mode == "edit":
            st.title("Edit your Profile")

            st.markdown("**Already registered?** Enter your email to sign back in.")
            returning_email = st.text_input("Your registered email", key="returning_email")
            if st.button("Sign in", use_container_width=True):
                if returning_email.strip():
                    existing = get_student_by_email(returning_email.strip())
                    if existing:
                        auth.persist_login("student", existing["id"])
                        st.session_state.mode = "view"
                        st.switch_page("pages/1_Profile.py")
                    else:
                        st.error("No account found with that email. Fill the form below to create one.")
                else:
                    st.warning("Please enter your email.")

            full_name = st.text_input("Full name", value=student["name"])
            st.markdown(f"Email: {student['email']} (can't be changed)") #email is the unique key in the db, we don't let users change it

            LinkedIn = st.text_input("LinkedIn profile URL", value=student["linkedin"] or "")
            Education = st.text_input("Current curriculum and name of the university", value=student["education"] or "")

            #parse the saved comma-separated interests back into a list for the multiselect
            saved_interests = [
                i.strip() for i in (student["interests"] or "").split(",") if i.strip()
            ]
            Interests = st.multiselect(
                "Your interests",
                options=[
                    "Marketing",
                    "Finance",
                    "Technology",
                    "Design",
                    "Data & Analytics",
                    "Legal",
                    "Human Resources",
                    "Coding",
                    "Consulting",
                    "Sustainability",
                ],
                default=saved_interests,
            )

            availability_options = [
                "Less than 5 hours / week",
                "5-10 hours / week",
                "10-20 hours / week",
                "Full-time",
                "Weekends only",
            ]
            saved_availability_index = (
                availability_options.index(student["availability"])
                if student["availability"] in availability_options else 0
            )
            Availability = st.selectbox(
                "Availability",
                options=availability_options,
                index=saved_availability_index,
            )

            Photo = st.file_uploader(
                "Profile picture",
                type=["png", "jpg", "jpeg"],
            )
            if Photo is not None:
                st.image(Photo, width=150)

            cv_file = st.file_uploader(
                "Upload your CV (PDF)",
                type=["pdf"],
            )
            if cv_file is not None:
                st.write(f"CV Uploaded: {cv_file.name}")

            col_back, col_save_profile = st.columns(2)
            with col_back: #to have a button that cancel changes if needed
                if st.button("Cancel", use_container_width=True):
                    st.session_state.mode = "view"
                    st.rerun()

            with col_save_profile:
                if st.button("Save Profile", use_container_width=True):
                    #only the name is still required
                    if not full_name.strip():
                        st.error("Name is required.")
                        st.stop()

                    #update the existing row in the database (NOT create_student)
                    update_student(
                        student["id"],
                        name=full_name.strip(),
                        linkedin=LinkedIn.strip() or None,
                        education=Education.strip() or None,
                        interests=", ".join(Interests) or None,
                        availability=Availability,
                    )

                    #if they uploaded a new CV, save it and update the filename
                    if cv_file is not None:
                        cv_filename = f"student_{student['id']}.pdf"
                        (UPLOADS / cv_filename).write_bytes(cv_file.getvalue())
                        update_student(student["id"], cv_filename=cv_filename)

                    #if they uploaded a new photo, save it
                    if Photo is not None:
                        (UPLOADS / f"student_{student['id']}_photo.png").write_bytes(Photo.getvalue())

                    #done - back to view mode
                    st.session_state.mode = "view"
                    st.success("Profile updated.")
                    st.rerun()

        # ===== VIEW MODE: read-only profile + Edit button =====
        else:
            st.title("Your Profile")
            st.caption("This is what startups see when you apply.")
            st.markdown(f"**Name:**  {student['name']}")
            st.markdown(f"**Email:**  {student['email']}")
            st.markdown(f"**LinkedIn:**  {student['linkedin'] or '—'}")
            st.markdown(f"**Education:**  {student['education'] or '—'}")
            st.markdown(f"**Interests:**  {student['interests'] or '—'}")
            st.markdown(f"**Availability:**  {student['availability'] or '—'}")
            st.markdown(f"**CV:**  {student['cv_filename'] or '—'}")
            if st.button("Edit Profile", type="primary", use_container_width=True):
                st.session_state.mode = "edit"
                st.rerun()

        st.stop()  #after either branch, stop so the signup form below doesn't render

            

        



#now we create the opening of the form once the user clicks on the button student
if st.session_state.role == "student" and st.session_state.mode == "edit":
    st.title("Student Profile")

    # ===== Email sign-in for returning students =====
    st.markdown("**Already registered?** Enter your email to sign back in.")
    returning_email = st.text_input("Your registered email", key="returning_email_signup")
    if st.button("Sign in", use_container_width=True, key="signin_existing"):
        if returning_email.strip():
            existing = get_student_by_email(returning_email.strip())
            if existing:
                auth.persist_login("student", existing["id"])
                st.session_state.mode = "view"
                st.switch_page("pages/1_Profile.py")
            else:
                st.error("No account found with that email. Fill the form below to create one.")
        else:
            st.warning("Please enter your email.")

    st.divider()

    st.markdown("**New here?** Create your student profile below.")

    full_name = st.text_input("Full name")
    email = st.text_input ("Email")
#second part of the form because we ask for the linkedin and university (same structure as name because we want the user to fill it out completely) and needs to be on the same allignment as the full name because it is part of the if statement 

    LinkedIn = st.text_input("LinkedIn profile URL")
    Education = st.text_input("Current curriculum and name of the university")
#okay now we have to use sth different because we want the user to choose between several options and not write sth down 
    Interests = st.multiselect(
        "Your interests",
        options=[
            "Marketing",
            "Finance",
            "Technology",
            "Design",
            "Data & Analytics",
            "Legal",
            "Human Resources",
            "Coding",
            "Consulting",
            "Sustainability",
        ],
    )
#now its more or less the same as the one with interest but we want the user to only choose one option and not multiple 
    Availability = st.selectbox(
        "Availability",
        options=[
            "Less than 5 hours / week",
            "5-10 hours / week",
            "10-20 hours / week",
            "Full-time",
            "Weekends only",
        ],
    )
#now we want to put the picture feature, it is different because the user has to upload sth 
    Photo = st.file_uploader(
        "Profile picture",
        type=["png", "jpg", "jpeg"],
    )
    if Photo is not None:
        st.image(Photo, width=150)
#okay now we do the same but for the CV 
    cv_file = st.file_uploader(
        "Upload your CV (PDF)",
        type=["pdf"],
    )
    if cv_file is not None:
        st.write(f"CV Uploaded: {cv_file.name}")

#now what we are doing is again creating a two columns thing to add a "back" and a "save profile" button
    col_back, col_save_profile = st.columns(2)

    with col_back:
        if st.button("Back", use_container_width=True):
            auth.clear_login()
            st.session_state.mode = "edit" #reset to edit for next time
            st.switch_page("app.py") #go back to the landing page (not just rerun, which would blank the screen)
    
    #when the user wants to save its profile 
    with col_save_profile: 
        if st.button("Save Profile", use_container_width=True):
            #we want the user to give us at least the namr and the email otherwise we won't save the profile:
            if not full_name.strip() or not email.strip():
                st.error("Name and email are required.")
                st.stop()
            
            #if a profile with this email already exists, don't create a new account but just sign back in, also typing your email is enough to go back
            existing = get_student_by_email(email.strip())
            if existing:
                auth.persist_login("student", existing["id"])
                st.session_state.mode = "view" #default to view mode for returning students
                st.info("Welcome back!")
                st.switch_page("pages/2_Discovery.py")

            #okay now if the user gave its name and email and isn't an already existing user, we want to save its profile
            #we need to create the profile, store it into the databasr and make sure that it goes into the students database
            student_id = create_student(
                name=full_name.strip(),
                email=email.strip(),
                linkedin=LinkedIn.strip() or None,
                cv_filename=None,                          
                education=Education.strip() or None,
                interests=", ".join(Interests) or None,    
                availability=Availability,
            )
            
            #if student uploaded a CV, it needs to be saved in the disk as uploads/students_<id>.pdf then update the database rowso it knows the filename
            if cv_file is not None: 
                cv_filename = f"student_{student_id}.pdf"
                (UPLOADS / cv_filename).write_bytes(cv_file.getvalue())
                update_student(student_id, cv_filename=cv_filename)

            #we basically do the same for the profile picture
            if Photo is not None: 
                (UPLOADS / f"student_{student_id}_photo.png").write_bytes(Photo.getvalue())

            #now we need to tell the rest of the app who is logged in. the accounts must appear in the other pages and "on the other side"
            auth.persist_login("student", student_id)
            st.session_state.mode = "view" #default to view mode after signup so coming back to Profile shows the saved info

            #once you're logged in and everything is saved, you need to receive the welcome email 
            student_row = get_student(student_id)
            subject, body = signup_confirm_student(student_row)
            send_email(student_row["email"], subject, body)

            #send tje user the job feed (discovery page)
            st.success("Profile created. Check your inbox for the confirmation email.")
            st.switch_page("pages/2_Discovery.py")

            
            
    
