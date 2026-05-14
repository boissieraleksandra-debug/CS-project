"""
3_Liked_Jobs.py — Saved jobs the student liked, with one-click Apply.
"""

import streamlit as st

import auth
import ui
from db import (
    init_db,
    list_liked_jobs,
    get_job,
    get_student,
    get_startup,
    create_application,
    remove_saved_job,
)
from mailer import send_email
from templates import (
    application_confirm_student,
    application_notify_startup,
)

# this sets up the page and loads the shared layout used across the app
st.set_page_config(page_title="Saved · gigly", page_icon="g", layout="centered", initial_sidebar_state="expanded")
init_db()
auth.restore_login()
ui.load_css()
ui.sidebar()

# checks that only student profiles have access
if st.session_state.get("role") != "student" or not st.session_state.get("student_id"):
    st.warning("Please create your student profile first.")
    if st.button("Go to Profile", type="primary", use_container_width=True):
        st.switch_page("pages/1_Profile.py")
    st.stop()

# here we get the id of the student who is currently logged in so we can load their saved jobs
student_id = st.session_state["student_id"]

# this is the title and short explanation shown at the top of the page
st.markdown("# Saved roles")
st.caption("Gigs you said yes to. Apply when you're ready — we'll email the startup for you.")
st.write("")


def send_application_emails(student_id, job_id):
    # here we load all the student, job, and startup data needed to build both application emails
    student = get_student(student_id)
    full_job = get_job(job_id)
    startup = get_startup(full_job["startup_id"])

    # this email confirms to the student that the application was saved and sent
    subject, body = application_confirm_student(student, full_job, startup)
    send_email(student["email"], subject, body)

    # this email tells the startup that a new student applied to one of their roles
    subject2, body2 = application_notify_startup(student, full_job, startup)
    send_email(startup["email"], subject2, body2)


def render_liked_job(job, student_id):
    # this function displays one saved job card, and it will be used again for each liked job with 
    with st.container(border=True):
        # if the job has an image, we show it at the top of the card to make the listing more visual
        if job["image_url"]:
            st.markdown(
                f"<div class='gigly-job-image-wrap'>"
                f"<div class='gigly-job-image' style=\"background-image:url('{job['image_url']}')\" aria-label='{job['title']}'></div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # here we show the main job information that the student sees first before opening more details
        st.caption(f"{job['startup_name']}  ·  {job['industry']}")
        st.markdown(f"### {job['title']}")
        st.caption(f"{job['location']}  ·  {job['duration']}")
        st.write(job["short_desc"])

        # this expandable section shows the full job details 
        with st.expander("View full description"):
            st.markdown("**About this role**")
            st.write(job["long_desc"])
            st.markdown("**What we're looking for**")
            st.write(job["requirements"])
            st.markdown(f"**Pay:**  {job['pay_rate']}")

        action_l, action_r = st.columns(2)

        with action_l:
            # if the student already applied, we show the status message instead of the Apply button
            if job["already_applied"]:
                st.success("Applied! We'll email you when the startup decides.")
            else:
                # when the student clicks Apply, we save the application in the database for this student and job
                if st.button("Apply", key=f"apply_{job['id']}",
                             type="primary", use_container_width=True):
                    app_id = create_application(student_id, job["id"])
                    if app_id is None:
                        st.warning("Already applied.")
                        st.rerun()

                    # after saving, we send email notifications to both sides so they know the application was created
                    send_application_emails(student_id, job["id"])
                    st.toast("Application sent.")
                    st.rerun()

        with action_r:
            # this button removes the job from the saved list without marking it as disliked
            if st.button("Remove", key=f"remove_{job['id']}", use_container_width=True):
                remove_saved_job(student_id, job["id"])
                st.toast("Removed from saved jobs.")
                st.rerun()


# here we load all jobs that this student liked before so we can show them on this page
liked = list_liked_jobs(student_id)
if not liked:
    # if no jobs were liked yet, we show a simple empty-state message and a button back to Discover
    st.info(
        "Nothing saved yet. Open **Discover**, save a few gigs, "
        "and they'll show up here."
    )
    if st.button("Go to Discover", type="primary", use_container_width=True):
        st.switch_page("pages/2_Discovery.py")
    st.stop()

# this loop goes through all liked jobs and uses the function above each time to show the jobs one by one
for job in liked:
    render_liked_job(job, student_id)
